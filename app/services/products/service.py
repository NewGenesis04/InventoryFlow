from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db
from app.db.models import Product, Stock
from app.db.schemas import ProductCreate, ProductResponse
from services.base import BaseService
import logging

logger = logging.getLogger(__name__)


class ProductService(BaseService):

    async def create_product(self, product: ProductCreate) -> ProductResponse:
        try:
            logger.info(f"Creating a new product with name: {product.name}")
            db_product = Product(**product.model_dump())
            self.db.add(db_product)
            await self.db.commit()
            await self.db.refresh(db_product)
            logger.info(f"Product created successfully with ID: {db_product.id}")

            # Create stock record
            stock = Stock(
                product_id=db_product.id,
                available_quantity=product.quantity,
                product_price=product.price,
                total_price=product.price * product.quantity
            )
            self.db.add(stock)
            await self.db.commit()
            logger.info(f"Stock added successfully with ID: {db_product.id}")
            return db_product
        except Exception as e:
            logger.error(f"Error occurred while creating product: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")