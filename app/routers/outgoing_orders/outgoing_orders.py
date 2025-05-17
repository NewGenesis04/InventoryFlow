import logging
from app.db.schemas import OutgoingOrderCreate, OutgoingOrderOut
from app.db.models import OutgoingOrder, Product, Stock
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db 

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/outgoing-orders", response_model=OutgoingOrderOut, status_code=status.HTTP_201_CREATED)
def create_outgoing_order(order: OutgoingOrderCreate, db: Session = Depends(get_db)):
    logger.info("Received request to create outgoing order: %s", order)

    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        logger.error("Product with ID %s not found", order.product_id)
        raise HTTPException(status_code=404, detail="Product not found")

    stock = db.query(Stock).filter(Stock.product_id == order.product_id).first()
    if not stock or stock.available_quantity < order.quantity:
        logger.error("Insufficient stock for product ID %s", order.product_id)
        raise HTTPException(status_code=400, detail="Insufficient stock")

    total_price = product.price * order.quantity
    outgoing_order = OutgoingOrder(**order.dict(), total_price=total_price)
    db.add(outgoing_order)

    # Deduct stock
    stock.available_quantity -= order.quantity
    stock.total_price = stock.product_price * stock.available_quantity

    db.commit()
    db.refresh(outgoing_order)

    logger.info("Outgoing order created successfully: %s", outgoing_order)
    return outgoing_order
