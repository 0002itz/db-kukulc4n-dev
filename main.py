from fastapi import FastAPI

from admin import router as admin_router
from users import router as users_router
from loginLogout import router as login_logout_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(login_logout_router, prefix="/login", tags=["login-logout"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O usa ["http://localhost:3000"] para un origen específico
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)