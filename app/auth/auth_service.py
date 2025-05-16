from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from fastapi import HTTPException, Depends
from app.db.schemas import AuthRegister, AuthLogin, AuthResponse
from app.utils import filter_user
from sqlalchemy.exc import SQLAlchemyError
from datetime import timedelta
from .auth_utils import hash_password, verify_password, authenticate_user, create_token
import logging
logger = logging.getLogger(__name__)
class AuthService():
    def __init__(self, db: AsyncSession):
        self.db = db
        
    
    async def register_user(self, request: AuthRegister) -> User:
        # Check if the user already exists
        existing_user_query = await filter_user(self.db, User.email == request.email)
        existing_user = existing_user_query.first()

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        try:
            # Hash the password and create a new user
            hashed_password = hash_password(request.password)
            new_user = User(
                username=request.username,
                email=request.email,
                role=request.role,
                password=hashed_password,
            )
            self.db.add(new_user)
            await self.db.commit()
            await self.db.refresh(new_user)

            return new_user
        except (SQLAlchemyError, Exception) as e:
            await self.db.rollback() 
            logger.error(f"Error creating user: {str(e)}")
            raise HTTPException(status_code=500, detail="Error creating new user")
    
    async def login_user(self, request: AuthLogin) -> AuthResponse:
        user = await authenticate_user(self.db, request.email, request.password)
        if not user:
            logger.error("Incorrect email or password")
            raise HTTPException(status_code=400, detail="Incorrect email or password"
                            )
        access_token = create_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=5))
        refresh_token = create_token(data={"sub": str(user.id)}, expires_delta=timedelta(days=7))

        return AuthResponse(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

