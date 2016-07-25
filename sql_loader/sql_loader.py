"""
 sql_loader.py

 Main class with logic for cloud database connection (see README)
 Author: Ishita Verma
 Date: 20 July 16

"""
import mysql.connector
from mysql.connector import Error
import table_queries as queries
import csv_reader as reader


def connect():
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect(host='mysql3.gear.host',
                                       database='datamonitor',
                                       user='datamonitor',
                                       password='datamonitor1!')

        if conn.is_connected():
            print('Connection established.')
            return conn

        else:
            print('Connection failed.')

    except Error as error:
        print(error)


def close_connect(conn):
    cursor = conn.cursor()
    cursor.close()
    conn.close()
    print('Connection closed.')


def run_queries():
    cursor = conn.cursor()

    for t in tables:
        if not queries.does_table_exist(cursor, t.tableName):
            queries.create_new_table(cursor, t)
            queries.fill_table_with_content(cursor, t)
            conn.commit()
            print("Added and filled new table to DB: " + t.tableName)
        else:
            print(t.tableName + " already exists")


if __name__ == '__main__':
    conn = connect()

    tables = reader.read_files()
    run_queries()

    close_connect(conn)
