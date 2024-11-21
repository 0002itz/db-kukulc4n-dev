from conectDB import getConectDB
from fastapi import APIRouter, HTTPException ,Form
import bcrypt

router = APIRouter()

@router.post("/newUser/{newUser}")
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

@router.get("/Userby/{nicknameOremail}")
async def user(nickname:str| None = None , emai:str | None = None): #opcional busqueda de correo o por nickname
    conn = getConectDB()
    c = conn.cursor()
    userdata = "SELECT userNickname,Email FROM Users WHERE userNickname=? OR Email=?;"
    c.execute(userdata,(nickname,emai))
    userdata = c.fetchone()
    c.close()
    if userdata is None:
        raise HTTPException(status_code=404, detail="User not found.")
    if emai:
        return {"User SELECT by Emay": userdata,}
    return { "User SELECT by Nickname": userdata }

@router.put("/newNickname/{Nickname}")
async def ChangNickname(newNickname:str,oldNickname:str):
    conn = getConectDB()
    c = conn.cursor()
    update="UPDATE Users SET userNickname = ? WHERE userNickname = ?;"
    c.execute(update,(newNickname,oldNickname,))
    conn.commit()
    c.close()
    return { "Nickname Update complet" : newNickname }

@router.put("/newEmail/{newEmail}")
async def ChangEmail(newEmail:str,oldEmail:str):
    conn = getConectDB()
    c = conn.cursor()
    update="UPDATE Email FROM Users WHERE Email = ?;"
    c.execute(update,(oldEmail,))
    emal = newEmail
    c.close()
    return { "Email update ": emal[0] }

@router.put("/newPw/{newPw}")
async def Changpasword(userNickname:str,newPw:str):
    conn = getConectDB()
    c = conn.cursor()
    pasword = b'newPw'
    salt = bcrypt.gensalt()
    desired_key_bytes = 32
    rounds = 200
    newPw = bcrypt.kdf(pasword, salt, desired_key_bytes, rounds)
    newpw = "UPDATE Users SET ps = ? WHERE usernickname=?"
    c.execute(newpw,(newPw,userNickname,))
    conn.commit()
    c.close()
    return { "New Password": newPw.hex() }