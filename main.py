from fastapi import FastAPI, HTTPException, Form,Depends
from conectDB import getConectDB

from admin import router as admin_router
from users import router as users_router
#from loginLogout import router as login_logout_router

app = FastAPI()

app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(users_router, prefix="/users", tags=["Users"])
#app.include_router(login_logout_router,prefix="/login", tags=["login-logout"])
