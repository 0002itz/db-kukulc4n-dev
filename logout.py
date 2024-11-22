from conectDB import getConectDB
from fastapi import APIRouter, HTTPException ,Form
#import bcrypt

router = APIRouter()

@router.post("/logout/")
async def login(Nickname:str=Form(...),pw:str=Form(...)):
    pass