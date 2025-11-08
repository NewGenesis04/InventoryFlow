from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db import schemas

class BaseService:
    def __init__(self, db: AsyncSession, current_user: Optional[schemas.User]):
        self.db = db
        self.user = current_user