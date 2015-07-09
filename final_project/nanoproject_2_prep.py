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

# Upper labels that are kept (from "nanoproject_2_query.py")
kept = ['maxspeed', 'access', 'address', 'amenity', 'entrance', 'natural', 'foot', 'name', 'ref', 'highway', 'barrier',
        'service', 'landuse', 'source', 'operator', 'building']


def update_name(name, mapping):
    street = name.split(" ")
    for i in range(0, len(street)):
        if street[i] in mapping:
            street[i] = mapping[street[i]]
    name = " ".join(street)
    return name


# Update the capitalization of these streets
mapping = {"chieftain": "Chieftain",
           "sweetpea": "Sweetpea"}
# Dictionary of labels
labels = {}


def shape_element(element):
    node = {}
    # Only add "nodes" and "ways"
    if element.tag == "node" or element.tag == "way":
        attributes = element.attrib
        # Tag this node with "node" or "way"
        node["type"] = element.tag
        for entry in attributes:
            # attributes in the CREATED array should be added under a key "created"
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
            else:
                node[entry] = attributes[entry]
        # Using second level tags
        for child in element:
            child_attributes = child.attrib
            for centry in child_attributes:
                if centry == "ref":
                    try:
                        node["node_refs"].append(child_attributes[centry])
                    except:
                        # Create a new list for "node_refs"
                        node["node_refs"] = [child_attributes[centry]]
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
                        try:
                            if ccentry not in labels[clabel]:
                                labels[clabel].append(ccentry)
                        except:
                            labels[clabel] = [ccentry]
                        try:
                            node[clabel][ccentry] = child_attributes["v"]
                        except:
                            # Create a new dictionary for node[clabel]
                            node[clabel] = {}
                            node[clabel][ccentry] = child_attributes["v"]
                        if ccentry == "street":
                            # Update street names, if needed
                            node["address"]["street"] = update_name(child_attributes["v"], mapping)
                    else:
                        # For upper labels
                        node[clabel] = child_attributes["v"]
                        if clabel not in labels:
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
                # if pretty:
                #     fo.write(json.dumps(el, indent=2) + "\n")
                # else:
                #     fo.write(json.dumps(el) + "\n")
    return data


def test():
    cam_data = process_map("cambridge_england.osm", True)
    print "The initial dictionary is"
    pprint.pprint(labels)

    print "The initial upper labels are:"
    pprint.pprint(labels.keys())

    kept_sub = {}
    for key in kept:
        kept_sub[key] = labels[key]

    print "The intermediate dictionary with sublabels is"
    pprint.pprint(kept_sub)

if __name__ == "__main__":
    test()
