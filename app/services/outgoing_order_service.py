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
        logger.info(f"Received request to create outgoing order: {order}")
        result = await self.db.execute(select(Product).where(Product.id == order.product_id))
        product = result.scalars().first()
        if not product:
            logger.error(f"Product with ID: {order.product_id} not found")
            raise HTTPException(status_code=404, detail="Product not found")

        total_price = product.price * order.quantity
        logger.info(f"Calculated total price: {total_price}")

        outgoing_order = OutgoingOrder(**order.model_dump(), total_price=total_price)
        self.db.add(outgoing_order)

        # Update stock
        stock_result = await self.db.execute(select(Stock).where(Stock.product_id == order.product_id))
        stock = stock_result.scalars().first()
        if stock:
            logger.info(f"Updating existing stock for product ID: {order.product_id}")
            stock.available_quantity -= order.quantity
            stock.total_price = stock.product_price * stock.available_quantity
        else:
            logger.info(f"Creating new stock record for product ID:  {order.product_id}")
            stock = Stock(
                product_id=product.id,
                available_quantity=-order.quantity,
                product_price=product.price,
                total_price=total_price
            )
            self.db.add(stock)

        await self.db.commit()
        await self.db.refresh(outgoing_order)
        logger.info(f"Outgoing order created successfully with ID: {outgoing_order.id}")
        return outgoing_order
    
    async def get_outgoing_order(self, order_id: int) -> OutgoingOrder:
        logger.info(f"Fetching outgoing order with ID: {order_id}")
        result = await self.db.execute(select(OutgoingOrder).where(OutgoingOrder.id == order_id))
        outgoing_order = result.scalars().first()
        if not outgoing_order:
            logger.error(f"Outgoing order with ID: {order_id} not found")
            raise HTTPException(status_code=404, detail="Outgoing order not found")
        return outgoing_order