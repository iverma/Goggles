"""
 csv_reader.py

 This class loads all CSV files and convert them into Table objects
 Author: Ishita Verma
 Date: 20 July 16

"""

import csv
import os
from Table import Table


def read_files():

    path = os.curdir+"/csv_files/"

    print(os.curdir)
    files = os.listdir(path)
    tables = []

    for file in files:
        if file.endswith(".csv"):

            t = Table("", "", "")

            # set table name from file name
            t.tableName = file.title()[:-4].lower()

            f = open(path + file)

            csv_f = csv.reader(f)
            csv_list = list(csv_f)

            # set headers and rest of data
            t.headers = csv_list[0]
            t.rows = csv_list[1:]

            tables.append(t)

    print_file_names(tables)
    return tables


def print_file_names(tables):

    csv_names = ""
    for row in tables:
        csv_names += row.tableName
        csv_names += ", "

    print("These were the CSV files that were loaded: " + csv_names[:-2])

