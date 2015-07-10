#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import re
import codecs
import json
import pprint

"""
This script is for the second nanoproject. It builds upon the scripts used in the Data Wrangling with
MongoDB class. The output should be a list of dictionaries that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

Initially, all labels are kept and printed to the JSON file. A "kept" array is generated from "nanoproject_2_query.py"
and is inserted in this file (manually). Afterwards, a dictionary of these kept labels and sublabels is generated to
further update the collection with MongoDB using "nanoproject_2_query.py".
"""

problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Sublabels that go in the created label
CREATED = ["version", "changeset", "timestamp", "user", "uid"]
# Sublabels that go in the position label
POSITION = ["lat", "lon"]

# Labels/sublabels that are kept
kept = {"address": ["street",
                 "postcode",
                 "housenumber",
                 "housename",
                 "city",
                 "country",
                 "interpolation"],
     "amenity": None,
     "barrier": None,
     "entrance": None,
     "foot": None,
     "highway": None,
     "landuse": None,
     "natural": None,
     "operator": None,
     "source": ["name"],
     "created": CREATED,
     "position": POSITION}

# Label structure for double-checking
labels = {}

def update_name(name, mapping):
    street = name.split(" ")
    for i in range(0, len(street)):
        if street[i] in mapping:
            street[i] = mapping[street[i]]
    name = " ".join(street)
    return name

def update_entry(entry, mapping):
    if entry in mapping:
        return mapping[entry]
    return entry

# Update the capitalization of these streets
mapping_street = {"chieftain": "Chieftain",
                  "sweetpea": "Sweetpea"}

# Update these cities
mapping_city = {"cambridge": "Cambridge",
                "South Cambridgeshire": "Cambridge",
                "Girton": "Cambridge",
                "11": "Cambridge"}
# Update barrier entries
mapping_barrier = {"fence;wall": "fence",
                   "fedr": None,
                   "bollards": "bollard"}

# Update entrance
mapping_entrance = {"secondary_entrance":"secondary",
                    "main_entrance; porters": "main_entrance;porters",
                    "porters;main_entrance": "main_entrance;porters",
                    "main": "main_entrance",
                    "emegency": "emergency",
                    "main_entrance;porters;": "main_entrance;porters"}
# Update highway
mapping_highway = {"bus_stand": "bus_stop"}

# Update landuse
mapping_landuse = {"institututional": "institutional"}

# Update operator
mapping_operator = {"YourSpace": "Your Space Apartments",
                    "Your Space": "Your Space Apartments",
                    "Trinity College": "Trinity College (University of Cambridge)",
                    "St John's College": "St John's College (University of Cambridge)",
                    "Lucy Cavendish College": "Lucy Cavendish College (University of Cambridge)",
                    "Lloyds": "Lloyds TSB",
                    "King's College": "King's College (University of Cambridge)",
                    "King's College (University Of Cambridge)": "King's College (University of Cambridge)",
                    "Needham Institute": "Needham Research Institute",
                    "Gonville and Caius College (University of Cambridge)": "Gonville & Caius College (University of Cambridge)",
                    "EDF": "EDF Energy",
                    "Clare College": "Clare College (University of Cambridge)",
                    "Christ's College": "Christ's College (University of Cambridge)"}

"""
After looking at the dataset, only the following labels will be kept:
    {"address": ["street",
                 "postcode",
                 "housenumber",
                 "housename",
                 "city",
                 "country",
                 "interpolation"],
     "amenity": None,
     "barrier": None,
     "entrance": None,
     "foot": None,
     "highway": None,
     "landuse": None,
     "natural": None,
     "operator": None,
     "source": ["name"],
     "created": ["version", "changeset", "timestamp", "user", "uid"],
     "position": ["lat", "lon"]}
"""
def shape_element(element):
    node = {}
    # Only add "nodes" and "ways"
    if element.tag == "node" or element.tag == "way":
        attributes = element.attrib
        # Tag this node with "node" or "way"
        node["type"] = element.tag
        # Upper labels are set
        for entry in attributes:
            # Attributes in the CREATED array should be added under a key "created"
            if entry in CREATED:
                try:
                    node["created"][entry] = attributes[entry]
                except:
                    # Create a new dictionary for created
                    node["created"] = {}
                    node["created"][entry] = attributes[entry]
            # Attributes for latitude and longitude are added to a "pos" array, for use in geospacial indexing.
            # The values inside "pos" arrays are floats and not strings.
            elif entry in POSITION:
                node["pos"] = [float(attributes["lat"]), float(attributes["lon"])]
            elif entry in kept:
                node[entry] = attributes[entry]
                labels[entry]= None
        # Using second level tags
        for child in element:
            child_attributes = child.attrib
            for centry in child_attributes:
                # Ignore ref label
                if centry == "ref":
                    pass
                elif centry == "k":
                    clabel = child_attributes[centry]
                    # If second level tag "k" value contains problematic characters, it is ignored
                    if problemchars.search(clabel):
                        pass
                    # Create second level tags
                    elif ":" in clabel:
                        col_index = clabel.index(":")
                        # Entry for second level tag
                        ccentry = clabel[col_index + 1:]
                        # Label for second level
                        clabel = clabel[0:col_index]
                        # Change "addr" to "address"
                        if clabel == "addr":
                            clabel = "address"
                        # Only keep labels and sublabels in the "kept dictionary"
                        if (clabel in kept) and (ccentry in kept[clabel]):
                            try:
                                node[clabel][ccentry] = child_attributes["v"]
                            except:
                                # Create a new dictionary for node[clabel]
                                node[clabel] = {}
                                node[clabel][ccentry] = child_attributes["v"]
                            try:
                                if ccentry not in labels[clabel]:
                                    labels[clabel].append(ccentry)
                            except:
                                labels[clabel] = [ccentry]
                            if ccentry == "street":
                            # Update street names, if needed
                                node["address"]["street"] = update_name(child_attributes["v"], mapping_street)
                            # If invalid postcode return None
                            elif ccentry == "postcode":
                                if (child_attributes["v"] == "CB1") or (child_attributes["v"] == "SG8 5TF"):
                                    return None
                            elif ccentry == "city":
                                # Update city to the one in the dictionary
                                node["address"]["street"] = update_entry(child_attributes["v"], mapping_city)
                    else:
                        # For upper labels
                        if clabel in kept:
                            if clabel == "barrier":
                                node[clabel] = update_entry(child_attributes["v"], mapping_barrier)
                            elif clabel == "entrance":
                                node[clabel] = update_entry(child_attributes["v"], mapping_entrance)
                            elif clabel == "highway":
                                node[clabel] = update_entry(child_attributes["v"], mapping_highway)
                            elif clabel == "landuse":
                                node[clabel] = update_entry(child_attributes["v"], mapping_landuse)
                            elif clabel == "operator":
                                node[clabel] = update_entry(child_attributes["v"], mapping_operator)
                            else:
                                node[clabel] = child_attributes["v"]
                            labels[clabel] = None
        return node
    else:
        return None

def process_map(file_in, pretty=False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


def test():
    cam_data = process_map("cambridge_england.osm", True)
    # pprint.pprint(labels)

if __name__ == "__main__":
    test()
