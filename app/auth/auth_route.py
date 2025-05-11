from fastapi import APIRouter, Depends
from .schemas import AuthRegister
from db.database import get_session
import logging
from .auth_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession

auth_logger = logging.getLogger(__name__)
auth_logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler("logs/auth.log")
file_handler.setFormatter(formatter)
auth_logger.addHandler(file_handler)

auth_route = APIRouter("/auth", tags=["auth"])

@auth_route.get("/register")
def register(user_data: AuthRegister, session:AsyncSession =Depends(get_session)):
    try:
        service = UserService(session=session)
        user = service.create_user(user_data)
        return user
    except Exception as e:
        logging.error(f"Error registering user: {e}")
        return {"message": "Error registering user"} 