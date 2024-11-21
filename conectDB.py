import sqlite3 as sql

def getConectDB():
    conn = sql.connect("./db/test-kuku.db")
    conn.row_factory = sql.Row
    return conn