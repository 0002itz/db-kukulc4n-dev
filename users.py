from conectDB import getConectDB

from fastapi import APIRouter, HTTPException ,Form , Path , Query, Body
from typing import Annotated
from pydantic import BaseModel
import bcrypt

class Post(BaseModel):
    nickname_Model: str
    date_post_Model: str
    title_post_Mdoel:str
    post_Model: str


router = APIRouter()

@router.post("/newUser/{newUser}")
async def create_user(*,
    Nickname: Annotated[str, Query(title="Verifide Nickname of New User.",max_length=20,min_length=8)] = ...,
    Email: Annotated[str, Query(title="Verifide Email of New User.",max_length=30,min_length=5)] = ...,
    pw: Annotated[str, Query(title="Verifide pW of New User.",max_length=30,min_length=5)] = ...,
    ):
    conn = getConectDB()
    c = conn.cursor()

    user_to_verified="SELECT userNickname FROM Users WHERE userNickname=?;"
    c.execute(user_to_verified,(Nickname,))
    user_data_fecth = c.fetchall()

    email_to_verified="SELECT Email FROM Users WHERE Email=?;"
    c.execute(email_to_verified,(Email,))
    email_data_fect=c.fetchone()

    user_verified=user_data_fecth
    email_verified=email_data_fect

    if user_verified:                   # Verificar si se encontró el usuario
        raise HTTPException(status_code=401, detail="User already exists.")

    if email_verified:
        raise HTTPException(status_code=401,detail="Emai already in use.")
    else:
        password = b'pw'
        salt = bcrypt.gensalt()
        pw = bcrypt.hashpw(password, salt)
    
        data_insert = "INSERT INTO Users (userNickname,Email,ps) Values (?,?,?);"
        c.execute(data_insert,(Nickname,Email,pw,))#,filter(Nickname==userNickname).first())
        conn.commit()
        c.close()
    
        user_create={ "User Created" : Nickname }
    
        if Email and pw:
            user_create.update({ "Email" : Email, "pw" : pw,})
    
    return user_create

@router.post("/newPost/{}")
async def create_post():
    conn = getConectDB()
    c = conn.cursor()

    post_Created=c.fetchall()
    c.close()

    return {"Post created" : post_Created }

@router.get("/userBy/{nicknameOremail}")
async def sherch_user_by_nickname_or_email(nickname:str| None = None , emai:str | None = None): #opcional busqueda de correo o por nickname
    conn = getConectDB()
    c = conn.cursor()

    user_nick_email_querry = "SELECT userNickname,Email FROM Users WHERE userNickname=? OR Email=?;"
    c.execute(user_nick_email_querry,(nickname,emai))
    c.close()

    userdata = c.fetchone()
    if userdata is None:
        raise HTTPException(status_code=404, detail="User not found.")
    if emai:
        return {"User SELECT by Emay": userdata,}

    return { "User SELECT by Nickname": userdata }

@router.put("/newNickname/{Nickname}")
async def chang_nickname(newNickname:str,oldNickname:str):
    conn = getConectDB()
    c = conn.cursor()

    creat_user_querry="UPDATE Users SET userNickname = ? WHERE userNickname = ?;"
    c.execute(creat_user_querry,(newNickname,oldNickname,))
    conn.commit()

    c.close()

    return { "Nickname Update complet" : newNickname }

@router.put("/newEmail/{newEmail}")
async def chang_email(newEmail:str,oldEmail:str):
    conn = getConectDB()
    c = conn.cursor()
    
    emal = newEmail
    update_email_querry="UPDATE Email FROM Users WHERE Email = ?;"
    c.execute(update_email_querry,(oldEmail,))
    conn.commit()

    c.close()

    return { "Email update ": emal[0] }

@router.put("/newPw/{newPw}")
async def chang_pasword(userNickname:str,newPw:str):
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