from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db
from app.db.models import IncomingOrder, Product, Stock
from app.db.schemas import IncomingOrderCreate, IncomingOrderResponse,IncomingOrderOut
from services.base import BaseService
import logging

logger = logging.getLogger(__name__)


class IncomingOrderService(BaseService):

    def create_incoming_order(self, order: IncomingOrderCreate):
        logger.info("Received request to create incoming order: %s", order)

        product = self.db.query(Product).filter(Product.id == order.product_id).first()
        if not product:
            logger.error("Product with ID %s not found", order.product_id)
            raise HTTPException(status_code=404, detail="Product not found")

        total_price = product.price * order.quantity
        logger.info("Calculated total price: %s", total_price)

        incoming_order = IncomingOrder(**order.model_dump(), total_price=total_price)
        self.db.add(incoming_order)

        # Update stock
        stock = self.db.query(Stock).filter(Stock.product_id == order.product_id).first()
        if stock:
            logger.info("Updating existing stock for product ID %s", order.product_id)
            stock.available_quantity += order.quantity
            stock.total_price = stock.product_price * stock.available_quantity
        else:
            logger.info("Creating new stock record for product ID %s", order.product_id)
            stock = Stock(
                product_id=product.id,
                available_quantity=order.quantity,
                product_price=product.price,
                total_price=total_price
            )
            self.db.add(stock)

        self.db.commit()
        self.db.refresh(incoming_order)
        logger.info("Incoming order created successfully with ID %s", incoming_order.id)
        return incoming_order