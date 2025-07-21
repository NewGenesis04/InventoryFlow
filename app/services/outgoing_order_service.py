from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db
from app.db.models import OutgoingOrder, Product, Stock
from app.db.schemas import OutgoingOrderCreate, IncomingOrderResponse
from app.services.base import BaseService
import logging

logger = logging.getLogger(__name__)


class OutgoingOrderService(BaseService):
    async def create_outgoing_order(self, order: OutgoingOrderCreate) -> IncomingOrderResponse:
        pass