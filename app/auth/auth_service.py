from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from fastapi import HTTPException, Depends
from app.db.schemas import AuthRegister
from app.utils import filter_user
from sqlalchemy.exc import SQLAlchemyError
from .auth_utils import hash_password, verify_password
import logging
logger = logging.getLogger(__name__)
class AuthService():
    def __init__(self, db: AsyncSession):
        self.db = db
        
    
    async def register_user(self, request: AuthRegister):
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
            raise HTTPException(
                status_code=500, detail="Error creating new user"
            )

