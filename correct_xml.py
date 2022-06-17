import xml.etree.ElementTree as ET
import argparse
document_loc = "/home/ubuntu/xml_edit/original.xml"


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


def check_for_dataset(dataset_id):
    tree = ET.parse("/media/data/customdocker/customvolumes/erddapContent/datasets.xml")
    root = tree.getroot()
    for child in root:
        if child.attrib:
            if "datasetID" in child.attrib:
                if child.attrib["datasetID"] == dataset_id:
                    raise ValueError(f"dataset {dataset_id} already present. Remove it from datasets.xml")


def update_doc(glider, mission, kind):
    """
    Edit the xml generated by GenerateDatasetsXml.sh
    :param glider: glider number
    :param mission: mission number
    :param kind: nrt or complete
    :return: 
    """
    tree = ET.parse(document_loc)
    root = tree.getroot()
    # Update dataset name
    ds_name = f"{kind}_SEA{str(glider).zfill(3)}_M{mission}"
    check_for_dataset(ds_name)
    root.attrib["datasetID"] = ds_name
    first_vars = []
    data_vars = []
    special_vars = ["longitude", "latitude", "time", "depth"]
    for child in root:
        # fix for addAttributes
        if child.tag == "addAttributes":
            add_attrs = child
            edit_add_attrs(add_attrs)
        if child.tag == "dataVariable":
            profile_index = False
            # Fix for the profile index
            for grand_child in child:
                if grand_child.tag == "sourceName" and grand_child.text == "profile_index":
                    profile_index = True
                if profile_index:
                    if grand_child.tag == "addAttributes":
                        print("got again")
                        child.remove(grand_child)
                        new_add = ET.Element("addAttributes")
                        add_element(new_add, "ioos_category", "Identifier")
                        add_element(new_add, "long_name", "Profile Index")
                        add_element(new_add, "cf_role", "timeseries_id")
                        child.append(new_add)
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
    for var in data_vars:
        root.append(var)

    # fix indentation and write xml
    ET.indent(tree, '  ')
    tree.write("/home/ubuntu/xml_edit/new.xml", encoding="utf-8", xml_declaration=True)

    # append dataset to datasets.xml
    tree_ds = ET.parse("/media/data/customdocker/customvolumes/erddapContent/datasets.xml")
    root_ds = tree_ds.getroot()
    root_ds.append(root)
    ET.indent(tree_ds, '  ')
    tree_ds.write("/media/data/customdocker/customvolumes/erddapContent/datasets.xml", encoding="utf-8",
                  xml_declaration=True)


def edit_add_attrs(adds):
    for child in adds:
        if child.attrib["name"] == "cdm_trajectory_variables":
            adds.remove(child)
    add_element(adds, "cdm_data_type", "TimeSeries")
    add_element(adds, "featureType", "TimeSeries")
    add_element(adds, "cdm_timeseries_variables", "profile_index")
    add_element(adds, "subsetVariables", "profile_index")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add dataset to ERDDAP')
    parser.add_argument('glider', type=int, help='glider number, e.g. 70')
    parser.add_argument('mission', type=int, help='Mission number, e.g. 23')
    parser.add_argument('kind', type=str, help='Kind of dataset, must be nrt or delayed')
    args = parser.parse_args()
    if args.kind not in ['nrt', 'delayed']:
        raise ValueError('kind must be nrt or delayed')
    update_doc(args.glider, args.mission, args.kind)
