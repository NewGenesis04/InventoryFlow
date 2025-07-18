import logging
from app.db.schemas import StockUpdate, StockResponse
from fastapi import APIRouter, Depends, HTTPException
from app.db.models import Stock
from sqlalchemy.orm import Session
from app.db.database import get_db 


logger = logging.getLogger(__name__)

router = APIRouter()


@router.patch("/stock/{id}", response_model=StockResponse, status_code=200)
def update_stock(id: int, stock_update: StockUpdate, db: Session = Depends(get_db)):
    logger.info(f"Received request to update stock with ID: {id}")

    stock = db.query(Stock).filter(Stock.id == id).first()
    if not stock:
        logger.error(f"Stock with ID {id} not found")
        raise HTTPException(status_code=404, detail="Stock not found")

    update_data = stock_update.model_dump(exclude_unset=True)
    logger.info(f"Update data: {update_data}")

    for key, value in update_data.items():
        setattr(stock, key, value)

    # Recalculate total_price if available_quantity or product_price is updated
    if "available_quantity" in update_data or "product_price" in update_data:
        stock.total_price = stock.product_price * stock.available_quantity

    db.commit()
    db.refresh(stock)

    logger.info(f"Successfully updated stock with ID {id}")
    return stock