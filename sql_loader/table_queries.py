"""
 table_queries.py

 SQL CRUD queries:

    1) does_table_exist
    2) create_new_table
    3) delete_table
    4) fill table with content (from Table object)
    5) delete all rows from table


 Author: Ishita Verma
 Date: 20 July 16

"""
# from Table import Table


def does_table_exist(cursor, table_name):
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.Tables;")
    row = cursor.fetchone()

    while row is not None:
        if table_name in row:
            return True
        row = cursor.fetchone()
    return False


def create_new_table(cursor, table):
    if does_table_exist(cursor, table.tableName):
        print("ERROR: create_new_table: " + table.tableName + " already exists")
        return False

    query = "CREATE TABLE " + table.tableName + " ( "
    for column in table.headers:
        query += column
        query += " varchar(255), "

    # remove last comma and close query
    query = query[:-2]
    query += " );"

    print("Creating new table to DB: " + table.tableName)
    cursor.execute(query)

    return True


def delete_table(cursor, table_name):
    cursor.execute("DROP TABLE " + table_name + ";")
    return 0


def fill_table_with_content(cursor, table):
    if not does_table_exist(cursor, table.tableName):
        print("ERROR: fill_table_with_content: " + table.tableName + " table does not exist. Cannot fill data")
        return False

    num_rows = len(table.rows)

    print "Filling %s new rows for table %s" % (num_rows, table.tableName)

    for i in range(0, num_rows):
        fill_row_with_content(cursor, table, i)
    return True


def fill_row_with_content(cursor, table, i):

    query = "INSERT INTO " + table.tableName + " VALUES( "
    for row in table.rows[i]:
        row = row.translate(None, '\'\"')
        query += "\""
        query += row
        query += "\", "

    # remove last comma and close query
    query = query[:-2]
    query += " );"

    cursor.execute(query)

    return True


def delete_all_rows(cursor, table):
    if does_table_exist(cursor, table.tableName):
        print("delete_all_rows:" + table.tableName + " does not exist")
        return False
    cursor.execute("TRUNCATE " + table.tableName + ";")
    return True



