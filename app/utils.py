import base64
from typing import Optional, Type
from sqlalchemy import select, asc, desc, Column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta, Query
from sqlalchemy.sql.elements import BinaryExpression
from app.db.models import User
from app.db.schemas import PaginatedResponse, Cursor

async def filter_user(db: AsyncSession, filter_condition: BinaryExpression):
    query = select(User).where(filter_condition)
    result = await db.execute(query)
    return result.scalars().first()

async def paginate(
    db: AsyncSession,
    model: Type[DeclarativeMeta],
    limit: int,
    after: Optional[str] = None,
    before: Optional[str] = None,
    sort_by: str = "id",
    query: Optional[Query] = None
) -> PaginatedResponse:
    """
    Performs cursor-based pagination on a SQLAlchemy model.
    """
    limit = min(100, limit)  # Enforce a max limit
    if query is None:
        query = select(model)
    
    sort_column: Column = getattr(model, sort_by, model.id)

    if after:
        try:
            decoded_cursor = base64.b64decode(after).decode()
            cursor_id = int(decoded_cursor)
            query = query.where(sort_column > cursor_id).order_by(asc(sort_column))
        except (ValueError, TypeError):
            # Handle invalid cursor
            pass
    elif before:
        try:
            decoded_cursor = base64.b64decode(before).decode()
            cursor_id = int(decoded_cursor)
            # When going backwards, we fetch in reverse order and then flip the results
            query = query.where(sort_column < cursor_id).order_by(desc(sort_column))
        except (ValueError, TypeError):
            # Handle invalid cursor
            pass
    else:
        # Default order for the first page
        query = query.order_by(asc(sort_column))

    # Fetch one more than the limit to see if there's a next page
    query = query.limit(limit + 1)
    result = await db.execute(query)
    items = result.scalars().all()

    has_more = len(items) > limit
    items = items[:limit]
    
    if before:
        # If we were going backwards, reverse the list to show correct order
        items.reverse()

    next_cursor = None
    if has_more or before:
        if items:
            next_cursor_val = getattr(items[-1], sort_by, items[-1].id)
            next_cursor = base64.b64encode(str(next_cursor_val).encode()).decode()

    prev_cursor = None
    if (after and items) or (has_more and not before):
        if items:
            prev_cursor_val = getattr(items[0], sort_by, items[0].id)
            prev_cursor = base64.b64encode(str(prev_cursor_val).encode()).decode()

    return PaginatedResponse(
        data=items,
        cursor=Cursor(next=next_cursor, prev=prev_cursor)
    )