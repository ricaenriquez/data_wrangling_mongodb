#!/usr/bin/env python
# -*- coding: utf-8 -*-
# So, the problem is that the gigantic file is actually not a valid XML, because
# it has several root elements, and XML declarations.
# It is, a matter of fact, a collection of a lot of concatenated XML documents.
# So, one solution would be to split the file into separate documents,
# so that you can process the resulting files as valid XML documents.

import xml.etree.ElementTree as ET
PATENTS = 'patent.data'

def get_root(fname):
    tree = ET.parse(fname)
    return tree.getroot()


def split_file(filename):
    # we want you to split the input file into separate files
    # each containing a single patent.
    # As a hint - each patent declaration starts with the same line that was causing the error
    # The new files should be saved with filename in the following format:
    # "{}-{}".format(filename, n) where n is a counter, starting from 0.

    f = open(filename, "r")
    data = []
    start = 0
    filenum = 0
    for row in f.readlines():
        if row.startswith("<?xml") & (start > 0):
            fname = "{}-{}".format(PATENTS, filenum)
            fsplit = open(fname, "w")
            for item in data:
                fsplit.write("%s\n" % item)
            fsplit.close()
            data = []
            filenum += 1
        data.append(row)
        start += 1
    fname = "{}-{}".format(PATENTS, filenum)
    fsplit = open(fname, "w")
    for item in data:
        fsplit.write("%s\n" % item)
    fsplit.close()
    f.close()

def test():
    split_file(PATENTS)
    for n in range(4):
        try:
            fname = "{}-{}".format(PATENTS, n)
            f = open(fname, "r")
            if not f.readline().startswith("<?xml"):
                print "You have not split the file {} in the correct boundary!".format(fname)
            f.close()
        except:
            print "Could not find file {}. Check if the filename is correct!".format(fname)


test()