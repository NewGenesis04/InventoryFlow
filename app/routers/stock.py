import logging
from app.db.schemas import StockUpdate, StockOut
from fastapi import APIRouter, Depends, HTTPException
from app.db.models import Stock
from sqlalchemy.orm import Session
from app.db.database import get_db 


logger = logging.getLogger(__name__)

router = APIRouter()

@router.patch("/stock/{id}", response_model=StockOut)
def update_stock(id: int, stock_update: StockUpdate, db: Session = Depends(get_db)):
    logger.info(f"Received request to update stock with ID: {id}")
    
    stock = db.query(Stock).filter(Stock.id == id).first()
    if not stock:
        logger.error(f"Stock with ID {id} not found")
        raise HTTPException(status_code=404, detail="Stock not found")

    logger.info(f"Updating stock with ID {id}: quantity={stock_update.quantity}")
    stock.available_quantity = stock_update.quantity
    stock.total_price = stock.product_price * stock_update.quantity
    db.commit()
    db.refresh(stock)
    
    logger.info(f"Successfully updated stock with ID {id}")
    return stock