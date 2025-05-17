from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db

class BaseService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db