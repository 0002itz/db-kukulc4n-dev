import sqlite3 as sql
from fastapi import FastAPI, HTTPException

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

@app.get("/userByID/{userID}")
async def getUserID(userID:int):
    conn = getConectDB()
    c = conn.cursor()
    c.execute( f'SELECT userID FROM Users WHERE userid={userID}' )
    userid = c.fetchone()
    c.close()
    if userid is None:
        raise HTTPException(status_code=404, detail="UserID not found.")
    return { "UserID": userid[0] }

@app.post("/createrUser/")
async def createUser(Nickname,Email,ps):
    conn = getConectDB()
    c = conn.cursor()
    ps = f.encrypt(b'ps')
    data_insert = "INSERT INTO Users (userNickname,Email,ps) Values (?,?,?);"
    c.execute(data_insert,(Nickname,Email,ps))
    newUser = c.fetchone()
    conn.commit()
    c.close()
    if newUser is None:
        raise HTTPException(status_code=202,detail="New User Create.")
    return{ "User Create": newUser }

@app.post("/upDatePW/")
async def apdate():
    pass

@app.delete("/delateUserByID/{userID}")
async def delateUserById(userID:int):
    conn = getConectDB()
    c = conn.cursor()
    data_delate = f'DELETE FROM Users WHERE userID={userID};'
    c.execute(data_delate)
    usertoDelate = c.fetchone()
    conn.commit()
    c.close()
    print("User Delate.")
    return { "User Delate": usertoDelate[0] }