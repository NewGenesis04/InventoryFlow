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
        logger.info(f"Received request to create incoming order: {order}")
        result = await self.db.execute(select(Product).where(Product.id == order.product_id))
        product = result.scalars().first()
        if not product:
            logger.error(f"Product with ID {order.product_id} not found")
            raise HTTPException(status_code=404, detail="Product not found")

        total_price = product.price * order.quantity
        logger.info(f"Calculated total price: {total_price}")

        incoming_order = IncomingOrder(**order.model_dump(), total_price=total_price)
        self.db.add(incoming_order)

        # Update stock
        stock_result = await self.db.execute(select(Stock).where(Stock.product_id == order.product_id))
        stock = stock_result.scalars().first()
        if stock:
            logger.info(f"Updating existing stock for product ID: {order.product_id}")
            stock.available_quantity += order.quantity
            stock.total_price = stock.product_price * stock.available_quantity
        else:
            logger.info(f"Creating new stock record for product ID:  {order.product_id}")
            stock = Stock(
                product_id=product.id,
                available_quantity=order.quantity,
                product_price=product.price,
                total_price=total_price
            )
            self.db.add(stock)

        await self.db.commit()
        await self.db.refresh(incoming_order)
        logger.info(f"Incoming order created successfully with ID: {incoming_order.id}")
        return incoming_order