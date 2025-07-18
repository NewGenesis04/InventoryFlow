import logging
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schemas import ProductCreate, ProductResponse
from app.db.database import get_db
from app.services.products_service import ProductService

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()
def get_product_service(db: AsyncSession = Depends(get_db)):
    return ProductService(db)

@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, service: ProductService = Depends(get_product_service)):
    logger.info("create_product endpoint called")
    try:
        return await service.create_product(product)
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
