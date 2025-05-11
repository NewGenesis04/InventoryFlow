from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import filter_user
from app.db.schemas import AuthRegister, AuthResponse
from app.db.models import User
from sqlalchemy.exc import SQLAlchemyError
from app.auth.auth_utils import hash_password, verify_access_token, verify_password, get_current_user
from db.database import get_db

from app.auth.auth_service import AuthService
import logging

logger = logging.getLogger(__name__)
def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)

auth_route = APIRouter("/auth", tags=["auth"])

@auth_route.post("/register", response_model=AuthResponse)
async def register(request: AuthRegister, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.register_user(request)