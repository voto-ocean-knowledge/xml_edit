import xml.etree.ElementTree as ET

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
    ds_name = f"SEA{str(glider).zfill(3)}_M{mission}_{kind}"
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
    for child in root.findall('dataVariable'):
        root.remove(child)
    for var in first_vars:
        root.append(var)
        print("add special")
    for var in data_vars:
        root.append(var)
        print("add normal")

    # fix indentation and write xml
    ET.indent(tree, '  ')
    tree.write("new.xml", encoding="utf-8", xml_declaration=True)


def edit_add_attrs(adds):
    for child in adds:
        if child.attrib["name"] == "cdm_trajectory_variables":
            adds.remove(child)
    add_element(adds, "cdm_data_type", "TimeSeries")
    add_element(adds, "featureType", "TimeSeries")
    add_element(adds, "cdm_timeseries_variables", "profile_index")
    add_element(adds, "subsetVariables", "profile_index")


if __name__ == '__main__':
    update_doc(55, 44, "nrt")
