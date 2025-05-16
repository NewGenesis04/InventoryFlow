from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schemas import AuthRegister, AuthResponse, User, AuthLogin
from app.db.models import User
from db.database import get_db

from app.auth.auth_service import AuthService
import logging

logger = logging.getLogger(__name__)

def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)

router = APIRouter("/auth", tags=["auth"])

@router.post("/register", response_model=User)
async def register(request: AuthRegister, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.register_user(request)

@router.post('/login', response_model=User)
async def login(request: AuthLogin, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.login_user(request)