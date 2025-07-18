from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schemas import AuthRegister, AuthResponse, AuthLogin, User
from app.db.database import get_db
from typing import Optional
from app.auth.auth_utils import get_current_user

from app.auth.auth_service import AuthService
import logging

logger = logging.getLogger(__name__)

def get_auth_service(require_user: bool = False):
    if require_user:
        async def _get_service(
            db: AsyncSession = Depends(get_db),
            current_user: User = Depends(get_current_user),
        ):
            return AuthService(db, current_user)
    else:
        async def _get_service(db: AsyncSession = Depends(get_db)):
            return AuthService(db, None)
    
    return _get_service


router = APIRouter()

@router.post("/register", response_model=User, status_code=201)
async def register(request: AuthRegister, service: AuthService = Depends(get_auth_service(False))):
    return await service.register_user(request)

@router.post('/login', response_model=AuthResponse, status_code=200)
async def login(request: AuthLogin, service: AuthService = Depends(get_auth_service(False))):
    return await service.login_user(request)

@router.get('/me', response_model=User, status_code=200)
async def current_user(service: AuthService = Depends(get_auth_service(True))):
    return await service.current_user()