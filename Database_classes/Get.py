import sqlite3
from sqlite3 import Error

from classes_network import Lineage

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

    for i in columns:
        query += i + ", "

    query = query[:-2] + " FROM " + table

    values = conn.execute(query).fetchall()


    #cursor.close()
    conn.close()

    return values

def do_query(query, db):
    conn = create_connection(db)

    values = conn.execute(query).fetchall()
    conn.commit()

    conn.close()

    return values

def delete_from_db(table, condition, db):
    conn = create_connection(db)

    query = "DELETE FROM " + table + " WHERE " + condition
    conn.execute(query)

    conn.close()

