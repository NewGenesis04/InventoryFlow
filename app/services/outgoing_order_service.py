from fastapi import HTTPException
from sqlalchemy.future import select
from typing import Optional
from app.db.models import OutgoingOrder, Product, Stock, Customer, OrderStatusEnum
from app.db.schemas import OutgoingOrderCreate, OutgoingOrderResponse, OutgoingOrderSummary, PaginatedResponse
from app.services.base import BaseService
from app.utils import paginate
from sqlalchemy.orm import selectinload
import logging

logger = logging.getLogger(__name__)


class OutgoingOrderService(BaseService):
    """
    Service for managing outgoing orders (customer orders).
    Automatically decreases stock when orders are created.
    """

    async def create_outgoing_order(self, order: OutgoingOrderCreate) -> OutgoingOrderResponse:
        """
        Create a new outgoing order and decrease stock quantity.
        """
        try:
            result = await self.db.execute(
                select(Stock).where(Stock.id == order.stock_id)
            )
            stock = result.scalars().first()
            if not stock:
                logger.warning(
                    "Stock not found for outgoing order",
                    extra={"extra_fields": {"stock_id": order.stock_id}}
                )
                raise HTTPException(status_code=404, detail="Stock not found")
            
            if stock.available_quantity < order.quantity:
                logger.warning(
                    "Insufficient stock for outgoing order",
                    extra={"extra_fields": {
                        "stock_id": order.stock_id,
                        "requested_quantity": order.quantity,
                        "available_quantity": stock.available_quantity
                    }}
                )
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock. Available: {stock.available_quantity}, Requested: {order.quantity}"
                )
            
            result = await self.db.execute(
                select(Product).where(Product.id == order.product_id)
            )
            product = result.scalars().first()
            if not product:
                logger.warning(
                    "Product not found for outgoing order",
                    extra={"extra_fields": {"product_id": order.product_id}}
                )
                raise HTTPException(status_code=404, detail="Product not found")
            
            result = await self.db.execute(
                select(Customer).where(Customer.id == order.customer_id)
            )
            customer = result.scalars().first()
            if not customer:
                logger.warning(
                    "Customer not found for outgoing order",
                    extra={"extra_fields": {"customer_id": order.customer_id}}
                )
                raise HTTPException(status_code=404, detail="Customer not found")
            
            unit_price = float(product.price) if product.price else 0
            total_price = unit_price * order.quantity
            
            new_order = OutgoingOrder(
                customer_id=order.customer_id,
                product_id=order.product_id,
                stock_id=order.stock_id,
                quantity=order.quantity,
                unit_price=unit_price,
                total_price=total_price,
                order_date=order.order_date,
                status=OrderStatusEnum.pending
            )
            
            stock.available_quantity -= order.quantity
            
            self.db.add(new_order)
            await self.db.commit()
            await self.db.refresh(new_order)
            
            result = await self.db.execute(
                select(OutgoingOrder)
                .options(
                    selectinload(OutgoingOrder.customer),
                    selectinload(OutgoingOrder.product)
                )
                .where(OutgoingOrder.id == new_order.id)
            )
            new_order = result.scalars().first()
            
            logger.info(
                "Outgoing order created and stock decreased",
                extra={"extra_fields": {
                    "order_id": new_order.id,
                    "customer_id": order.customer_id,
                    "product_id": order.product_id,
                    "quantity": order.quantity,
                    "stock_remaining": stock.available_quantity,
                    "total_price": total_price
                }}
            )
            
            return OutgoingOrderResponse.model_validate(new_order)
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                "Error creating outgoing order",
                extra={"extra_fields": {"error": str(e)}}
            )
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    async def get_all_outgoing_orders(self, limit: int, after: Optional[str] = None, before: Optional[str] = None) -> PaginatedResponse[OutgoingOrderSummary]:
        """
        Retrieve all outgoing orders.
        """
        try:
            paginated_orders = await paginate(
                db=self.db,
                model=OutgoingOrder,
                limit=limit,
                after=after,
                before=before
            )
            if not paginated_orders.data:
                logger.warning("No outgoing orders found in database")
                raise HTTPException(status_code=404, detail="No outgoing orders found")
            
            logger.info(
                "Outgoing orders retrieved",
                extra={"extra_fields": {"total_orders": len(paginated_orders.data)}}
            )
            return paginated_orders
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                "Error fetching outgoing orders",
                extra={"extra_fields": {"error": str(e)}}
            )
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    async def get_outgoing_order_by_id(self, order_id: int) -> OutgoingOrderResponse:
        """
        Retrieve a specific outgoing order by ID.
        """
        try:
            result = await self.db.execute(
                select(OutgoingOrder)
                .options(
                    selectinload(OutgoingOrder.customer),
                    selectinload(OutgoingOrder.product)
                )
                .where(OutgoingOrder.id == order_id)
            )
            order = result.scalars().first()
            if not order:
                logger.warning(
                    "Outgoing order not found",
                    extra={"extra_fields": {"order_id": order_id}}
                )
                raise HTTPException(status_code=404, detail=f"Outgoing order with id {order_id} not found")

            if self.user.role == "customer" and order.customer.user_id != self.user.id:
                raise HTTPException(status_code=403, detail="Not authorized to view this order")
            
            logger.info(
                "Outgoing order retrieved",
                extra={"extra_fields": {
                    "order_id": order.id,
                    "customer_id": order.customer_id,
                    "product_id": order.product_id,
                    "quantity": order.quantity
                }}
            )
            return OutgoingOrderResponse.model_validate(order)
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                "Error fetching outgoing order",
                extra={"extra_fields": {"order_id": order_id, "error": str(e)}}
            )
            raise HTTPException(status_code=500, detail="Internal Server Error")
