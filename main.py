import sqlite3 as sql
from fastapi import FastAPI, HTTPException, Form
import bcrypt

app = FastAPI()

def getConectDB():
    conn = sql.connect("./db/test-kuku.db")
    conn.row_factory = sql.Row
    return conn

@app.get("/users/")
async def allUsers():
    conn = getConectDB()
    c = conn.cursor()
    c.execute( "SELECT * FROM Users" )
    users = c.fetchall()
    c.close()
    return { "AllUsers": users }

@app.post("/newUser/{newUser}")
async def createUser(Nickname:str = Form(...),Email:str = Form(...),pw:str = Form(...)):
    conn = getConectDB()
    c = conn.cursor()
    pasword = b'pw'
    salt = bcrypt.gensalt()
    desired_key_bytes = 32
    rounds = 200
    pw = bcrypt.kdf(pasword, salt, desired_key_bytes, rounds)
    data_insert = "INSERT INTO Users (userNickname,Email,ps) Values (?,?,?);"
    c.execute(data_insert,(Nickname,Email,pw,))
    conn.commit()
    c.close()
    return{ "User Create": Nickname ,"Email":Email }

@app.get("/Userby/{nicknameOremail}")
async def user(nicknameORemail:str,):
    conn = getConectDB()
    c = conn.cursor()
    userdata = "SELECT * FROM Users WHERE userNickname=? OR Email=?;"
    c.execute(userdata,(nicknameORemail,nicknameORemail))
    #c.execute(f'SELECT * FROM Users WHERE userNickname={nicknameORemail} OR Email={nicknameORemail};')
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

@app.put("/newPw/{newPw}")
async def Changpasword(userNickname:str,newPw:str):
    conn = getConectDB()
    c = conn.cursor()
    #oldpw = "SELECT ps FROM Users WHERE userNickname=?;"
    #c.execute(oldpw,(userNickname,))
    newPw = f.encrypt(b'newPw')
    newpw = "UPDATE Users SET ps = ? WHERE usernickname=?"
    c.execute(newpw,(newPw,userNickname,))
    conn.commit()
    c.close()
    return { "New Password": newpw }

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