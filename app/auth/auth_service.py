from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from .schemas import UserCreate, UserUpdate
from .auth_utils import hash_password, verify_password
class UserService():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id):
        user =  await self.session.query(User).filter(User.id == user_id).first()
        

    async def get_user_by_email(self, email):
        return await self.session.query(User).filter(User.email == email).first()
    
    async def check_if_user_exists(self, email):
        user = await self.session.query(User).filter(User.email == email).first()
        return user is not None
    
    async def create_user(self, user_data: UserCreate):
        
        user = await self.check_if_user_exists(user_data.email)
        if user:
            raise ValueError("User already exists")
        user_data.password = hash_password(user_data.password)
        user = User(**user_data.model_dump())
        self.session.add(user)
        await self.session.commit()
        return user

    async def update_user(self, user_id: int, user_data: UserUpdate):
        user = await self.session.query(User).filter(User.id == user_id).first()
        for key, value in user_data.model_dump().items():
            setattr(user, key, value)
        await self.session.commit()
        return user

    async def delete_user(self, user_id):
        user = await self.session.get(User, user_id)
        await self.session.delete(user)
        await self.session.commit()
        return user