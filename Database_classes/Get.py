import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def database_get(table, columns, db):
    conn = create_connection(db)

    query = "SELECT "
    #column1, column2, columnN FROM table_name;"

    for i in columns:
        query += i + ", "

    query = query[:-2] + " FROM " + table

    cur = conn.cursor()

    values = conn.execute(query).fetchall()


    #cursor.close()
    conn.close()

    return values
