import logging
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db.schemas import ProductCreate, ProductOut
from app.db.models import Product, Stock
from app.db.database import get_db

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/products", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        logger.info("Creating a new product with name: %s", product.name)
        db_product = Product(**product.model_dump())  # Updated to use model_dump
        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        stock = Stock(
            product_id=db_product.id,
            available_quantity=product.quantity,
            product_price=product.price,
            total_price=product.price * product.quantity
        )
        db.add(stock)
        db.commit()
        logger.info("Product created successfully with ID: %s", db_product.id)
        return db_product
    except Exception as e:
        logger.error("Error occurred while creating product: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
