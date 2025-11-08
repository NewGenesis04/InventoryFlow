from fastapi import HTTPException
from sqlalchemy.future import select
from typing import List
from app.db.models import Stock
from app.db.schemas import StockUpdate, StockResponse, StockSummary
from app.services import BaseService
from sqlalchemy.orm import selectinload
import logging

logger = logging.getLogger(__name__)


class StockService(BaseService):
    """
    Service for managing stock operations.
    Handles retrieving stock levels and manual adjustments.
    """

    async def get_all_stocks(self) -> List[StockSummary]:
        """
        Retrieve all stock entries.
        """
        try:
            result = await self.db.execute(select(Stock))
            stocks = result.scalars().all()
            if not stocks:
                logger.warning("No stock entries found in database")
                raise HTTPException(status_code=404, detail="No stock entries found")
            
            logger.info(
                "Stock entries retrieved",
                extra={"extra_fields": {"total_stocks": len(stocks)}}
            )
            return stocks

        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                "Error fetching stock entries",
                extra={"extra_fields": {"error": str(e)}}
            )
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def get_stock_by_id(self, stock_id: int) -> StockResponse:
        """
        Retrieve a specific stock entry by ID.
        """
        try:
            result = await self.db.execute(
                select(Stock)
                .options(selectinload(Stock.product))
                .where(Stock.id == stock_id)
            )
            stock = result.scalars().first()
            if not stock:
                logger.warning(
                    "Stock entry not found",
                    extra={"extra_fields": {"stock_id": stock_id}}
                )
                raise HTTPException(status_code=404, detail=f"Stock with id {stock_id} not found")
            
            logger.info(
                "Stock entry retrieved",
                extra={"extra_fields": {
                    "stock_id": stock.id,
                    "product_id": stock.product_id,
                    "available_quantity": stock.available_quantity
                }}
            )
            return StockResponse.model_validate(stock)

        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                "Error fetching stock entry",
                extra={"extra_fields": {"stock_id": stock_id, "error": str(e)}}
            )
            raise HTTPException(status_code=500, detail="Internal Server Error")

    async def update_stock(self, stock_id: int, stock_update: StockUpdate) -> StockResponse:
        """
        Manually adjust stock quantity (PATCH operation).
        This is for manual stock adjustments, not for order-based changes.
        """
        try:
            result = await self.db.execute(
                select(Stock)
                .options(selectinload(Stock.product))
                .where(Stock.id == stock_id)
            )
            stock = result.scalars().first()
            if not stock:
                logger.warning(
                    "Stock entry not found for update",
                    extra={"extra_fields": {"stock_id": stock_id}}
                )
                raise HTTPException(status_code=404, detail=f"Stock with id {stock_id} not found")
            
            old_quantity = stock.available_quantity
            
            for key, value in stock_update.model_dump(exclude_unset=True).items():
                setattr(stock, key, value)
            
            await self.db.commit()
            await self.db.refresh(stock)

            logger.info(
                "Stock entry updated",
                extra={"extra_fields": {
                    "stock_id": stock_id,
                    "product_id": stock.product_id,
                    "old_quantity": old_quantity,
                    "new_quantity": stock.available_quantity,
                    "adjustment": stock.available_quantity - old_quantity
                }}
            )

            return StockResponse.model_validate(stock)

        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                "Error updating stock entry",
                extra={"extra_fields": {"stock_id": stock_id, "error": str(e)}}
            )
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Internal Server Error")