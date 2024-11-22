from fastapi import FastAPI, HTTPException, Form
from conectDB import getConectDB

from admin import router as admin_router
from users import router as users_router
from login import router as login_router
from logout import router as logout_router

app = FastAPI()

app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(login_router,prefix="/login", tags=["login"])
app.include_router(logout_router,prefix="/logout", tags=["logout"])