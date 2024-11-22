from conectDB import getConectDB
from fastapi import APIRouter, HTTPException, Form
import bcrypt

router = APIRouter()

@router.post("/login/{nicknameANDpw}")
async def login(Nickname: str = Form(...), pw: str = Form(...)):
    # Establecer conexión a la base de datos
    conn = getConectDB()
    c = conn.cursor()

    # Consulta para obtener la contraseña del usuario
    password_query = "SELECT ps FROM Users WHERE userNickname=?"
    c.execute(password_query, (Nickname,))
    
    # Obtener el resultado de la consulta
    password_query = c.fetchone()

    # Cerrar conexión
    c.close()
    conn.commit()

    # Verificar si se encontró el usuario
    if not password_query:
        return {"Message": "User not found!"}

    # La contraseña almacenada se encuentra en password_query[0]
    stored_password = password_query[0]  # Es la contraseña en su formato original (no hex)

    # Compara la contraseña ingresada con la almacenada usando bcrypt
    if bcrypt.checkpw(pw.encode('utf-8'), stored_password):
        return {"User validate": Nickname, "Message": "Password matches!"}
    else:
        return {"User validate": Nickname, "Message": "Invalid password"}
    
