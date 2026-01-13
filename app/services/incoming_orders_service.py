from fastapi import HTTPException
from sqlalchemy.future import select
from typing import List, Optional
from app.db.models import IncomingOrder, Product, Stock, Supplier, OrderStatusEnum
from app.db.schemas import IncomingOrderCreate, IncomingOrderResponse, IncomingOrderSummary, IncomingOrderStatusUpdate, PaginatedResponse
from app.services.base import BaseService
from app.utils import paginate
from sqlalchemy.orm import selectinload
import logging

logger = logging.getLogger(__name__)


class IncomingOrderService(BaseService):
    """
    Service for managing incoming orders (supplier orders).
    Automatically creates/updates stock when orders are created.
    """

    async def create_incoming_order(self, order: IncomingOrderCreate) -> IncomingOrderResponse:
        """
        Create a new incoming order and create/update stock entry.
        """
        try:
            result = await self.db.execute(
                select(Product).where(Product.id == order.product_id)
            )
            product = result.scalars().first()
            if not product:
                logger.warning(
                    "Product not found for incoming order",
                    extra={"extra_fields": {"product_id": order.product_id}}
                )
                raise HTTPException(status_code=404, detail="Product not found")
            
            result = await self.db.execute(
                select(Supplier).where(Supplier.id == order.supplier_id)
            )
            supplier = result.scalars().first()
            if not supplier:
                logger.warning(
                    "Supplier not found for incoming order",
                    extra={"extra_fields": {"supplier_id": order.supplier_id}}
                )
                raise HTTPException(status_code=404, detail="Supplier not found")
            
            total_cost = order.unit_cost * order.quantity
            
            new_order = IncomingOrder(
                supplier_id=order.supplier_id,
                product_id=order.product_id,
                batch_number=order.batch_number,
                quantity=order.quantity,
                unit_cost=order.unit_cost,
                total_cost=total_cost,
                supply_date=order.supply_date,
                status=OrderStatusEnum.pending
            )
            
            self.db.add(new_order)
            await self.db.commit()
            await self.db.refresh(new_order)
            
            new_stock = Stock(
                product_id=order.product_id,
                incoming_order_id=new_order.id,
                batch_number=order.batch_number,
                available_quantity=order.quantity,
                expiry_date=order.expiry_date
            )
            
            self.db.add(new_stock)
            await self.db.commit()
            await self.db.refresh(new_stock)
            
            result = await self.db.execute(
                select(IncomingOrder)
                .options(
                    selectinload(IncomingOrder.supplier),
                    selectinload(IncomingOrder.product)
                )
                .where(IncomingOrder.id == new_order.id)
            )
            new_order = result.scalars().first()
            
            logger.info(
                "Incoming order created and stock increased",
                extra={"extra_fields": {
                    "order_id": new_order.id,
                    "supplier_id": order.supplier_id,
                    "product_id": order.product_id,
                    "batch_number": order.batch_number,
                    "quantity": order.quantity,
                    "stock_id": new_stock.id,
                    "total_cost": total_cost
                }}
            )
            
            return IncomingOrderResponse.model_validate(new_order)
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                "Error creating incoming order",
                extra={"extra_fields": {"error": str(e)}}
            )
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    async def get_all_incoming_orders(self, limit: int, after: Optional[str] = None, before: Optional[str] = None) -> PaginatedResponse[IncomingOrderSummary]:
        """
        Retrieve all incoming orders.
        """
        try:
            paginated_orders = await paginate(
                db=self.db,
                model=IncomingOrder,
                limit=limit,
                after=after,
                before=before
            )
            if not paginated_orders.data:
                logger.warning("No incoming orders found in database")
                raise HTTPException(status_code=404, detail="No incoming orders found")
            
            logger.info(
                "Incoming orders retrieved",
                extra={"extra_fields": {"total_orders": len(paginated_orders.data)}}
            )
            return paginated_orders
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                "Error fetching incoming orders",
                extra={"extra_fields": {"error": str(e)}}
            )
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    async def get_incoming_order_by_id(self, order_id: int) -> IncomingOrderResponse:
        """
        Retrieve a specific incoming order by ID.
        """
        try:
            result = await self.db.execute(
                select(IncomingOrder)
                .options(
                    selectinload(IncomingOrder.supplier),
                    selectinload(IncomingOrder.product)
                )
                .where(IncomingOrder.id == order_id)
            )
            order = result.scalars().first()
            if not order:
                logger.warning(
                    "Incoming order not found",
                    extra={"extra_fields": {"order_id": order_id}}
                )
                raise HTTPException(status_code=404, detail=f"Incoming order with id {order_id} not found")
            
            if self.user.role == "supplier" and order.supplier.user_id != self.user.id:
                raise HTTPException(status_code=403, detail="Not authorized to view this order")
            
            logger.info(
                "Incoming order retrieved",
                extra={"extra_fields": {
                    "order_id": order.id,
                    "supplier_id": order.supplier_id,
                    "product_id": order.product_id,
                    "quantity": order.quantity
                }}
            )
            return IncomingOrderResponse.model_validate(order)
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                "Error fetching incoming order",
                extra={"extra_fields": {"order_id": order_id, "error": str(e)}}
            )
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_my_incoming_orders(self, limit: int, after: Optional[str] = None, before: Optional[str] = None) -> PaginatedResponse[IncomingOrderSummary]:
        """
        Retrieve all incoming orders for the current supplier.
        """
        try:
            result = await self.db.execute(
                select(Supplier).where(Supplier.user_id == self.user.id)
            )
            supplier = result.scalars().first()
            if not supplier:
                raise HTTPException(status_code=404, detail="Supplier profile not found for current user")

            query = select(IncomingOrder).where(IncomingOrder.supplier_id == supplier.id)
            paginated_orders = await paginate(
                db=self.db,
                model=IncomingOrder,
                limit=limit,
                after=after,
                before=before,
                query=query
            )

            if not paginated_orders.data:
                raise HTTPException(status_code=404, detail="No incoming orders found for this supplier")
            
            return paginated_orders
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                "Error fetching incoming orders for supplier",
                extra={"extra_fields": {"user_id": self.user.id, "error": str(e)}}
            )
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def update_incoming_order_status(self, order_id: int, status_update: IncomingOrderStatusUpdate) -> IncomingOrderResponse:
        """
        Update the status of an incoming order.
        """
        try:
            result = await self.db.execute(
                select(IncomingOrder)
                .options(
                    selectinload(IncomingOrder.supplier),
                    selectinload(IncomingOrder.product)
                )
                .where(IncomingOrder.id == order_id)
            )
            order = result.scalars().first()
            if not order:
                raise HTTPException(status_code=404, detail=f"Incoming order with id {order_id} not found")

            if self.user.role == "supplier" and order.supplier.user_id != self.user.id:
                raise HTTPException(status_code=403, detail="Not authorized to update this order")

            order.status = status_update.status
            await self.db.commit()
            await self.db.refresh(order)
            
            logger.info(
                "Incoming order status updated",
                extra={"extra_fields": {
                    "order_id": order.id,
                    "new_status": order.status
                }}
            )
            return IncomingOrderResponse.model_validate(order)
        
        except HTTPException:
            raise
        except Exception as e:
            await self.db.rollback()
            logger.error(
                "Error updating incoming order status",
                extra={"extra_fields": {"order_id": order_id, "error": str(e)}}
            )
            raise HTTPException(status_code=500, detail="Internal Server Error")
