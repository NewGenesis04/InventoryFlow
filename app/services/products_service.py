from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db
from app.db.models import Product, Stock
from app.db.schemas import ProductCreate, ProductResponse
from app.services.base import BaseService
import logging

logger = logging.getLogger(__name__)


class ProductService(BaseService):

    async def create_product(self, product: ProductCreate) -> ProductResponse:
        pass