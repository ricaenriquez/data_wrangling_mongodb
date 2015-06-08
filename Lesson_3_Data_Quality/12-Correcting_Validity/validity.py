"""
Your task is to check the "productionStartYear" of the DBPedia autos datafile for valid values.
The following things should be done:
- check if the field "productionStartYear" contains a year
- check if the year is in range 1886-2014
- convert the value of the field to be just a year (not full datetime)
- the rest of the fields and values should stay the same
- if the value of the field is a valid year in range, as described above,
  write that line to the output_good file
- if the value of the field is not a valid year, 
  write that line to the output_bad file
- discard rows (neither write to good nor bad) if the URI is not from dbpedia.org
- you should use the provided way of reading and writing data (DictReader and DictWriter)
  They will take care of dealing with the header.

You can write helper functions for checking the data and writing the files, but we will call only the 
'process_file' with 3 arguments (inputfile, output_good, output_bad).
"""
import csv
import pprint
from pandas import *
import datetime as dt

INPUT_FILE = 'autos.csv'
OUTPUT_GOOD = 'autos-valid.csv'
OUTPUT_BAD = 'FIXME-autos.csv'

def process_file(input_file, output_good, output_bad):

    df = read_csv(input_file)
    # Remove Nulls
    bad_df = df[df['productionStartYear'].isnull()]
    df = df[df['productionStartYear'].notnull()]
    # Remove the line with word 'Year'
    bad_df = bad_df.append(df[df['productionStartYear'].str.contains('Year')])
    df = df[~df['productionStartYear'].str.contains('Year')]
    df['productionStartYear'] = df['productionStartYear'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S+%U:%W').year)
    bad_df = bad_df.append(df[(df['productionStartYear'] < 1886) | (df['productionStartYear'] > 2014)])
    df = df[(df['productionStartYear'] >= 1886) & (df['productionStartYear'] <= 2014)]
    df = df[df['URI'].str.contains('dbpedia.org')]
    bad_df = bad_df[bad_df['URI'].str.contains('dbpedia.org')]

    bad_df.to_csv(output_bad)
    df.to_csv(output_good)

def test():
    process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)

if __name__ == "__main__":
    test()