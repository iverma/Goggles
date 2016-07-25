"""
 Table.py

 Table class is representation of data loaded from CSV
 Author: Ishita Verma
 Date: 20 July 16

"""


class Table:
    def __init__(self, tableName, headers, rows):
        self.tableName = tableName
        self.headers = headers
        self.rows = rows

