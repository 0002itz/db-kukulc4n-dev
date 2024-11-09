from enum import Enum
from fastapi import FastAPI

import sqlite3 as sql
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

app = FastAPI()

def getConectDB():
    conn = sql.connect("../db/test-kuku.db")
    conn.row_factory = sql.Row
    return conn

@app.get("/Users/")
def getUsers():
    conn = getConectDB()
    c = conn.cursor()
    c.execute( "SELECT * FROM Users" )
    users = c.fetchall()
    conn.close()
    return {"users": [dict(user) for user in users]}