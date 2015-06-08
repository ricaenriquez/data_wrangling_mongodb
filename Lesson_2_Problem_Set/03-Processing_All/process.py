#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Let's assume that you combined the code from the previous 2 exercises
# with code from the lesson on how to build requests, and downloaded all the data locally.
# The files are in a directory "data", named after the carrier and airport:
# "{}-{}.html".format(carrier, airport), for example "FL-ATL.html".
# The table with flight info has a table class="dataTDRight".
# There are couple of helper functions to deal with the data files.
# Please do not change them for grading purposes.
# All your changes should be in the 'process_file' function
from bs4 import BeautifulSoup
from zipfile import ZipFile
import os

datadir = "data"


def open_zip(datadir):
    with ZipFile('{0}.zip'.format(datadir), 'r') as myzip:
        myzip.extractall()


def process_all(datadir):
    files = os.listdir(datadir)
    return files


def process_file(f):
    # This is example of the datastructure you should return
    # Each item in the list should be a dictionary containing all the relevant data
    # Note - year, month, and the flight data should be integers
    # You should skip the rows that contain the TOTAL data for a year
    # data = [{"courier": "FL",
    #         "airport": "ATL",
    #         "year": 2012,
    #         "month": 12,
    #         "flights": {"domestic": 100,
    #                     "international": 100}
    #         },
    #         {"courier": "..."}
    # ]
    data = []
    info = {}
    info["courier"], info["airport"] = f[:6].split("-")
    
    with open("{}/{}".format(datadir, f), "r") as html:

        soup = BeautifulSoup(html)
        datas = soup.find_all("td",attrs={"style":"font-family: Verdana, Geneva, Arial, Helvetica, sans-serif;"})
        k = 0
        h = 0
        clean_data = []
        for entry in datas:
            if ('total' in entry.string.lower()):
                # print "total found"
                for l in range(h,k-1):
                    clean_data.append(datas[l])
                h = k + 4
            k += 1
        j = 0
        for i in range(0,len(clean_data)/5):
            # print clean_data[j+0].string
            # print clean_data[j+1].string
            # print clean_data[j+2].string
            # print clean_data[j+3].string

            year = int(clean_data[j+0].string)
            month = int(clean_data[j+1].string)
            domestic = int((clean_data[j+2].string).replace(',',''))
            international = int((clean_data[j+3].string.replace(',','')))
            data.append({"courier": info["courier"],
                    "airport": info["airport"],
                    "year": year,
                    "month": month,
                    "flights": {"domestic": domestic,
                                "international": international}})
            j += 5

    return data


def test():
    print "Running a simple test..."
    # open_zip(datadir)
    files = process_all(datadir)
    data = []
    for f in files:
        data += process_file(f)
    assert len(data) == 3
    for entry in data[:3]:
        assert type(entry["year"]) == int
        assert type(entry["flights"]["domestic"]) == int
        assert len(entry["airport"]) == 3
        assert len(entry["courier"]) == 2
    print "... success!"

if __name__ == "__main__":
    test()