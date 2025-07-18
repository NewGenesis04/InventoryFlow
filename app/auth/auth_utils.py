from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.utils import filter_user
from app.config import settings
from typing import List
from app.db import schemas
from app.db.database import get_db
from app.db.models import User
from jose import JWTError, jwt
import logging

logger = logging.getLogger(__name__)
http_scheme = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def verify_access_token(token: HTTPAuthorizationCredentials = Depends(http_scheme)) -> dict:
    try:
        payload = jwt.decode(token.credentials, settings.JWT_SECRET_KEY,
                             algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError as e:
        logger.error(f"Invalid token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
    
def create_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(
            timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
async def authenticate_user(db: AsyncSession, email: str, password: str):   
    #Retrieve the first result asynchronously
    query = await filter_user(db, User.email == email)
    user = await query.first()

    #Verify the user and password
    if user is None or not verify_password(password, user.password):
        logger.warning("Authentication failed")
        return False

    return user

async def get_current_user(token: HTTPAuthorizationCredentials = Depends(http_scheme), db: AsyncSession = Depends(get_db)) -> schemas.User:
    try:
        payload = verify_access_token(token) 
        user_id: int = payload.get("sub")
        if not user_id:
            print("No user_id specified")
            raise HTTPException(status_code=401, detail="Invalid token")
        user_id = int(user_id)

        query = await filter_user(db, User.id == user_id)
        current_user = await query.first()
        if not current_user:
            print("No user found in database")
            raise HTTPException(status_code=401, detail="User not found")
        
        return schemas.User.model_validate(current_user)
    except JWTError as e:
        logger.error(f"JWT Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

def role_required(required_roles: List[str]) -> bool:
    def role_checker(current_user: schemas.User = Depends(get_current_user)):
        if current_user.role not in required_roles:
            logger.warning(f"User {current_user.username} does not have the required role(s): {required_roles}")
            raise HTTPException(status_code=403, detail="Operation not permitted")
        return True
    return role_checker
