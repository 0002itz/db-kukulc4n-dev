from conectDB import getConectDB


from typing import Annotated
from fastapi import APIRouter, HTTPException ,Form , Path , Query, Body, Depends
#from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel,Field
#from passlib.context import CryptContext
import bcrypt
from passlib.hash import pbkdf2_sha256

class Post(BaseModel):
    user_nickname_Model: str
    date_post_Model: str
    title_post_Mdoel:str
    post_Model: str

router = APIRouter()

class User(BaseModel):
    Nickname: Annotated[str, Body(title="Verifide Nickname of New User.",max_length=20,min_length=8)]=Field(examples=["Carlos Vallarta"])
    Email: Annotated[str, Body(title="Verifide Email of New User.",max_length=30,min_length=5)]=Field(examples=["foo@gamil.com"])
    pw: Annotated[str, Body(title="Verifide pW of New User.",max_length=30,min_length=5)]=Field(examples=["ExampleOfPasWord"])
    disabled: Annotated[bool, Body(title="autorizado?",default=1)]=Field(examples=["1"])

@router.post("/newUser/{newUser}")
async def create_user(user: User):
    conn = getConectDB()
    c = conn.cursor()

    def user_verifier():                   # Verificar si se encontró el usuario
        user_to_verified_querry="SELECT userNickname FROM Users WHERE userNickname=?;"
        c.execute(user_to_verified_querry,(user.Nickname,))
        user_data_fecth = c.fetchall()
        user_exist=user_data_fecth
        if user_exist:
            raise HTTPException(status_code=401, detail="User already exists.")

    def email_verifier():
        email_to_verified_query="SELECT Email FROM Users WHERE Email=?;"
        c.execute(email_to_verified_query,(user.Email,))
        data_fect=c.fetchone()
        email_verified=data_fect
        if email_verified:
            raise HTTPException(status_code=401,detail="Emai already in use.")

    def password_hasher():
        pw = pbkdf2_sha256.hash(user.pw)
        return pw
        #return pwd_context.hash(user.pw)

    user_verifier()
    email_verifier()
    pw_hash=password_hasher()

    data_insert = "INSERT INTO Users (userNickname,Email,pw,disabled) Values (?,?,?,?);"
    c.execute(data_insert,(user.Nickname,user.Email,pw_hash,user.disabled))#,filter(Nickname==userNickname).first())
    conn.commit()
    c.close()

    user_create={ "User Created" : user.Nickname }

    if user.Email and user.pw:
        user_create.update({ "Email" : user.Email,})
    
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
    userdata = c.fetchone()
    c.close()

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
async def chang_pasword(newPw:str,userNickname:str,):
    conn = getConectDB()
    c = conn.cursor()

    #hash_password = b'newPw'
    #salt = bcrypt.gensalt()
    #newPw = bcrypt.hashpw(hash_password, salt)
    #pw_hash = pbkdf2_sha256.hash(newPw)
    password = newPw
    pw_hash = pbkdf2_sha256.hash(password)
    newPw=pw_hash

    newpw_querry = "UPDATE Users SET pw = ? WHERE usernickname=?"
    c.execute(newpw_querry,(newPw,userNickname,))
    conn.commit()

    c.close()

    return { "Password change of": userNickname }