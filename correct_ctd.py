import xml.etree.ElementTree as ET
import argparse
import logging
import subprocess

from correct_xml import add_element, edit_datavar_add_attrs, correct_charset

_log = logging.getLogger(__name__)


def edit_add_attrs(adds):
    for child in adds:
        if child.attrib["name"] == "cdm_trajectory_variables":
            adds.remove(child)
        if child.attrib["name"] == "subsetVariables":
            adds.remove(child)

    add_element(adds, "cdm_data_type", "TimeSeries")
    add_element(adds, "featureType", "TimeSeries")
    add_element(adds, "cdm_timeseries_variables", "cast_number")
    add_element(adds, "subsetVariables", "cast_number")


def update_doc(dataset_id):
    """
    Edit the xml generated by GenerateDatasetsXml.sh for ctd datasets
    """

    document_loc = f"/home/usrerddap/erddap/xml_edit/xml/{dataset_id}.xml"
    tree = ET.parse(document_loc)
    root = tree.getroot()
    root.attrib["datasetID"] = dataset_id
    correct_charset(root)

    first_vars = []
    data_vars = []
    special_vars = ["longitude", "latitude", "time", "depth", "cast_number"]
    for child in root:
        # fix for addAttributes
        if child.tag == "addAttributes":
            add_attrs = child
            edit_add_attrs(add_attrs)
        if child.tag == "dataVariable":
            profile_index = False
            # Fix for the profile index
            for grand_child in child:
                if grand_child.tag == "sourceName" and grand_child.text == "cast_number":
                    profile_index = True
                if profile_index:
                    if grand_child.tag == "addAttributes":
                        child.remove(grand_child)
                        new_add = ET.Element("addAttributes")
                        add_element(new_add, "ioos_category", "Identifier")
                        add_element(new_add, "long_name", "Cast number")
                        add_element(new_add, "cf_role", "timeseries_id")
                        child.append(new_add)
                # Correct addAttributes
                if grand_child.tag == "addAttributes":
                    _log.debug(f"Remove units from {child[0].text}")
                    grand_child = edit_datavar_add_attrs(grand_child)

                # Take the common selection variables and put them at the top
                if grand_child.tag == "sourceName":
                    if grand_child.text in special_vars:
                        first_vars.append(child)
                    else:
                        data_vars.append(child)
    # remove data variables
    for child in root.findall('dataVariable'):
        root.remove(child)
    # re-append data variables in desired order
    for var in first_vars:
        root.append(var)
    vars_dict = {}
    for var in data_vars:
        for child in var:
            if child.tag == "sourceName":
                vars_dict[child.text] = var
    vars_dict_sorted = dict(sorted(vars_dict.items()))
    for var in vars_dict_sorted.values():
        root.append(var)

    # fix indentation and write xml
    ET.indent(tree, '  ')
    out = f"/home/usrerddap/erddap/content/parts/{dataset_id}.xml"
    tree.write(out, encoding="utf-8", xml_declaration=True)
    _log.info(f"Recombining datasets.xml")
    subprocess.check_call(['/usr/bin/bash', "/home/usrerddap/erddap/xml_edit/make_datasets.sh"])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Correct xml for ctd dataset')
    parser.add_argument('dataset_id', type=str, help='dataset id')
    args = parser.parse_args()
    logf = f'/data/log/ctd.log'
    logging.basicConfig(filename=logf,
                        filemode='a',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    _log.info(f"Start add dataset {args.dataset_id} to xml")
    update_doc(args.dataset_id)
    _log.info(f"Complete add dataset {args.dataset_id} to xml")
