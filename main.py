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

@app.post("/newUser/{newUser}")
async def createUser(Nickname,Email,ps):
    conn = getConectDB()
    c = conn.cursor()
    ps = f.encrypt(b'ps')
    data_insert = "INSERT INTO Users (userNickname,Email,ps) Values (?,?,?);"
    c.execute(data_insert,(Nickname,Email,ps,))
    conn.commit()
    c.close()
    return{ "User Create": Nickname }

@app.get("/allUsers/{Users}")
async def allUsers():
    conn = getConectDB()
    c = conn.cursor()
    c.execute( "SELECT * FROM Users" )
    users = c.fetchall()
    c.close()
    return { "AllUsers": users }

@app.get("/User/{userID}")
async def user(userID:int):
    conn = getConectDB()
    c = conn.cursor()
    userdata = "SELECT * FROM Users WHERE userID=?;"
    c.execute(userdata,(userID,))
    userdata = c.fetchone()
    c.close()
    if userdata is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return { "User SELECT": userdata }

@app.put("/newNickname/{Nickname}")
async def ChangNickname(newNickname:str,oldNickname:str):
    conn = getConectDB()
    c = conn.cursor()
    update="UPDATE Users SET userNickname = ? WHERE userNickname = ?;"
    c.execute(update,(newNickname,oldNickname,))
    conn.commit()
    c.close()
    return { "Nickname Update complet" : newNickname }

@app.put("/newEmail/{newEmail}")
async def ChangEmail(newEmail:str,oldEmail:str):
    conn = getConectDB()
    c = conn.cursor()
    update="UPDATE Email FROM Users WHERE Email = ?;"
    c.execute(update,(oldEmail,))
    emal = newEmail
    c.close()
    return { "Email update ": emal[0] }

@app.put("/newpw/{Newpw}")
async def newpasword(userNickname:str):
    conn = getConectDB()
    c = conn.cursor()
    userdata = "SELECT ps FROM Users WHERE userNickname=?;"
    c.execute(userdata,(userNickname,))
    ps=c.fetchone()
    #ps.f.decrypt()
    conn.commit()
    c.close()
    return { "New Password": ps }

@app.delete("/delateUser/{userID}")
async def delateUser(userID:int):
    conn = getConectDB()
    c = conn.cursor()
    data_delate = f'DELETE FROM Users WHERE userID={userID};'
    c.execute(data_delate)
    conn.commit()
    c.close()
    print("User Delate.")
    return { "User Delate": f'ID {userID}' }