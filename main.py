from enum import Enum
from fastapi import FastAPI, HTTPException

import sqlite3 as sql
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

app = FastAPI()

def getConectDB():
    conn = sql.connect("./db/test-kuku.db")
    conn.row_factory = sql.Row
    return conn

@app.get("/users/")
async def getUsers():
    conn = getConectDB()
    c = conn.cursor()
    c.execute( "SELECT * FROM Users" )
    users = c.fetchall()
    conn.close()
    return { "AllUsers": users }

@app.get("/users/{userID}")
async def getUserID(userID:int):
    conn = getConectDB()
    c = conn.cursor()
    c.execute( f'SELECT userID FROM Users WHERE userid={userID}' )
    userid = c.fetchone()
    conn.close()
    if userid is None:
        raise HTTPException(status_code=404, detail="UserID not found")
    return { "UserID": userid[0] }