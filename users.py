from conectDB import getConectDB
from fastapi import APIRouter, HTTPException ,Form
import bcrypt

router = APIRouter()

@router.post("/newUser/{newUser}")
async def createUser(Nickname:str = Form(...),Email:str = Form(...),pw:str = Form(...)):
    conn = getConectDB()
    c = conn.cursor()
    password = b'pw'
    salt = bcrypt.gensalt()
    pw = bcrypt.hashpw(password, salt)
    data_insert = "INSERT INTO Users (userNickname,Email,ps) Values (?,?,?);"
    c.execute(data_insert,(Nickname,Email,pw,))
    conn.commit()
    c.close()
    return{ "User Create": Nickname ,"Email":Email }

@router.get("/Userby/{nicknameOremail}")
async def user(nickname:str| None = None , emai:str | None = None): #opcional busqueda de correo o por nickname
    conn = getConectDB()
    c = conn.cursor()
    user_nick_email_querry = "SELECT userNickname,Email FROM Users WHERE userNickname=? OR Email=?;"
    c.execute(user_nick_email_querry,(nickname,emai))
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
    creat_user_querry="UPDATE Users SET userNickname = ? WHERE userNickname = ?;"
    c.execute(creat_user_querry,(newNickname,oldNickname,))
    conn.commit()
    c.close()
    return { "Nickname Update complet" : newNickname }

@router.put("/newEmail/{newEmail}")
async def ChangEmail(newEmail:str,oldEmail:str):
    conn = getConectDB()
    c = conn.cursor()
    emal = newEmail
    update_email_querry="UPDATE Email FROM Users WHERE Email = ?;"
    c.execute(update_email_querry,(oldEmail,))
    conn.commit()
    c.close()
    return { "Email update ": emal[0] }

@router.put("/newPw/{newPw}")
async def Changpasword(userNickname:str,newPw:str):
    conn = getConectDB()
    c = conn.cursor()
    hash_password = b'newPw'
    salt = bcrypt.gensalt()
    newPw = bcrypt.hashpw(hash_password, salt)
    newpw_querry = "UPDATE Users SET ps = ? WHERE usernickname=?"
    c.execute(newpw_querry,(newPw,userNickname,))
    conn.commit()
    c.close()
    return { "New Password": newPw }