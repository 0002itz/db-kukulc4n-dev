from conectDB import getConectDB
from fastapi import APIRouter, HTTPException, Form
import bcrypt

router = APIRouter()

@router.post("/login/{nicknameANDpw}")
async def login(Nickname: str = Form(...), pw: str = Form(...)):
    conn = getConectDB()
    c = conn.cursor()
    password_query = "SELECT ps FROM Users WHERE userNickname=?"
    c.execute(password_query, (Nickname,))
    password_query = c.fetchone()
    c.close()
    stored_password = password_query[0]
    if not password_query:                   # Verificar si se encontró el usuario
        raise HTTPException(status_code=404, detail="User not found.")
    if bcrypt.checkpw(pw.encode('utf-8'), stored_password):# Compara la contraseña ingresada con la almacenada usando bcrypt
        return {"User validate": Nickname, "Message": "Password matches!"}
    raise HTTPException(status_code=404, detail="Invalid password.")
