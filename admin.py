from conectDB import getConectDB
from fastapi import APIRouter
import bcrypt

router = APIRouter()

@router.get("/users/")
async def allUsers():
    conn = getConectDB()
    c = conn.cursor()
    c.execute( "SELECT * FROM Users" )
    users = c.fetchall()
    c.close()
    decoded_users = []
    for user in users:
        user_data = {
            "userID": user[0],
            "nickname": user[1],
            "email": user[2],
            "password_hash": user[3].hex() if isinstance(user[3], bytes) else user[3]
        }
        decoded_users.append(user_data)
    return { "AllUsers": decoded_users }

@router.delete("/delateUser/{userID}")
async def delateUser(userID:int):
    conn = getConectDB()
    c = conn.cursor()
    data_delate = f'DELETE FROM Users WHERE userID={userID};'
    c.execute(data_delate)
    conn.commit()
    c.close()
    print("User Delate.")
    return { "User Delate": f'ID {userID}' }