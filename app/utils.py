from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import BinaryExpression
from app.db.models import User

async def filter_user(db: AsyncSession, filter_condition: BinaryExpression):
    query = select(User).where(filter_condition)
    result = await db.execute(query)
    return result.scalars()