import subprocess
import xml.etree.ElementTree as ET
import xarray as xr
import datetime
from pathlib import Path
import database


def add_element(tree, name, text):
    """
    Add elements to an xml object
    :param tree: xml object to append to
    :param name: name attribute of the item
    :param text: text of the item to add
    :return: tree with appended item
    """
    new = ET.Element("att")
    new.attrib["name"] = name
    new.text = text
    tree.append(new)


def edit_add_attrs_og(adds):
    for child in adds:
        if child.attrib["name"] == "cdm_trajectory_variables":
            adds.remove(child)
        if child.attrib["name"] == "subsetVariables":
            adds.remove(child)

    add_element(adds, "cdm_data_type", "Trajectory")
    add_element(adds, "cdm_trajectory_variables", "TRAJECTORY")

def erddap_generate_xml(glider, mission, file_dir):
    bash_cmd = fr"""
    set -e
    cd /usr/local/tomcat/webapps/erddap/WEB-INF/
    java -cp classes:../../../lib/servlet-api.jar:lib/* -Xms12000M -Xmx12000M gov.noaa.pfel.erddap.GenerateDatasetsXml EDDTableFromMultidimNcFiles /Data/{file_dir}/{glider}/M{mission}/timeseries .\* nothing default default default default default default default default default default default default default default default default
    """


    result = subprocess.run(
        ["docker", "exec", "-i", "voto-erddap-1", "bash", "-c", bash_cmd],
        capture_output=True,
        text=True,
        check=True
    )

    output = result.stdout
    if 'java.lang.RuntimeException' in output:
        return False
    else:
        return True


def convert_xml(glider, mission, file_dir):
    data_dir = Path(f'/data/{file_dir}/{glider}/M{mission}/timeseries')
    if not data_dir.exists():
        print("no dir")
        return
    infiles = list(data_dir.glob('*.nc'))
    if len(infiles) != 1:
        print("bad infiles")
        return
    ds = xr.open_dataset(infiles[0])
    document_loc = f"/data/erddapDataNew/logs/GenerateDatasetsXml.out"
    tree = ET.parse(document_loc)
    root = tree.getroot()
    ds_name = ds.attrs['id']
    root.attrib["datasetID"] = ds_name
    for child in root:
        # fix for addAttributes
        if child.tag == "addAttributes":
            add_attrs = child
            edit_add_attrs_og(add_attrs)

    # fix indentation and write xml
    ET.indent(tree, '  ')
    out = f"/home/usrerddap/erddap_compose/erddap/content/parts/{ds_name}.xml"
    tree.write(out, encoding="utf-8", xml_declaration=True)


def make_datasets_xml():
    # Read in datasets_base_xml for the header settings (no datasets)
    repo_dir = Path('/home/usrerddap/erddap_compose/')
    xml_file = repo_dir / 'erddap' / 'content' / 'datasets_base.xml'
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # remove any datasets entered into the base xml
    for child in root.findall('dataset'):
        root.remove(child)
    # loop through input datasets and add them to the xml
    parts_dir = repo_dir / 'erddap' / 'content' / 'parts'
    parts_files = list(parts_dir.glob('*xml'))
    parts_files.sort()
    for fn in parts_files:
        source_tree = ET.parse(fn)
        source_root = source_tree.getroot()
        root.append(source_root)

    # Write this out to datasets.xml
    ET.indent(tree, '  ')
    out = repo_dir / 'erddap' / 'content' / 'datasets.xml'
    tree.write(out, encoding="utf-8", xml_declaration=True)


def process_all_og1(kind='nrt', days=3):
    time_cut = datetime.datetime.now() - datetime.timedelta(days=days)
    file_dir = 'OG_complete' if kind == 'delayed' else 'OG_nrt'
    infiles = list(Path(f'/data/{file_dir}/').rglob('*.nc'))
    infiles = [file for file in infiles if 'timeseries' in str(file)]
    infiles.sort()
    for infile in infiles:
        print(infile)
        parts = infile.parts
        glider = parts[3]
        mission = int(parts[4][1:])
        mission_id = f'{kind}_{glider}_M{mission}'
        last_proc_time = database.last_processed_time(mission_id)
        if last_proc_time > time_cut:
            continue
        xml_generated = erddap_generate_xml(glider, mission, file_dir)
        if not xml_generated:
            continue
        convert_xml(glider, mission, file_dir)
        database.update_processed_time(mission_id, datetime.datetime.now())


if __name__ == '__main__':
    process_all_og1()
    make_datasets_xml()
