from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db
from app.db.models import IncomingOrder, Product, Stock
from app.db.schemas import IncomingOrderCreate, IncomingOrderResponse
from app.services.base import BaseService
import logging

logger = logging.getLogger(__name__)


class IncomingOrderService(BaseService):

    async def create_incoming_order(self, order: IncomingOrderCreate) -> IncomingOrderResponse:
        pass