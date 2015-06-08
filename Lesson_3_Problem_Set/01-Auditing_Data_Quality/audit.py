#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.
In the first exercise we want you to audit the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- 'NoneType' if the value is a string "NULL" or an empty string ""
- 'list', if the value starts with "{"
- 'int', if the value can be cast to int
- 'float', if the value can be cast to float, but is not an int
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and the datatypes that can be found in the field.
All the data initially is a string, so you have to do some checks on the values first.

"""
import codecs
import csv
import json
import pprint
import pandas as pd

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label", "isPartOf_label", "areaCode", "populationTotal", 
          "elevation", "maximumElevation", "minimumElevation", "populationDensity", "wgs84_pos#lat", "wgs84_pos#long", 
          "areaLand", "areaMetro", "areaUrban"]

def check_int(n):
    possibilities ='01234567890+-'
    for entry in n:
        if entry not in possibilities:
            return False
    return True

def check_float(n):
    possibilities ='01234567890+-e.'
    for entry in n:
        if entry not in possibilities:
            return False
    return True

def audit_file(filename, fields):
    fieldtypes = {}

    df = pd.read_csv(filename)
    for key in fields:
        types = []
        nulls = df[df[key].isnull()][key]
        if len(nulls) > 0:
            types.append(type(None))
        notnulls = df[df[key].notnull()][key]
        lists = notnulls[notnulls.map(lambda x: x.startswith('{'))]
        if len(lists) > 0:
            types.append(type([]))
        remains = notnulls[~notnulls.map(lambda x: x.startswith('{'))]
        ints = remains[remains.map(lambda x: check_int(x))]
        if len(ints) > 0:
            types.append(type(0))
        remains2 = remains[~remains.isin(ints)]
        floats = remains2[remains2.map(lambda x: check_float(x))]
        if len(floats) > 0:
            types.append(type(1.1))
        # strs = remains2[~remains2.isin(floats)]
        # if len(strs) > 0:
        #     types.append(type('hello'))
        fieldtypes[key] = set(types)
    return fieldtypes


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    # pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])
    
if __name__ == "__main__":
    test()
