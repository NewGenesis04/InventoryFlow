import logging
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schemas import ProductCreate, ProductResponse, User
from app.db.database import get_db
from app.auth.auth_utils import get_current_user
from app.services.products_service import ProductService

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

def get_product_service(require_user: bool = False):
    if require_user:
        async def _get_service(
            db: AsyncSession = Depends(get_db),
            current_user: User = Depends(get_current_user),
        ):
            return ProductService(db, current_user)
    else:
        async def _get_service(db: AsyncSession = Depends(get_db)):
            return ProductService(db, None)
    
    return _get_service

@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, service: ProductService = Depends(get_product_service(True))):
    logger.info("create_product endpoint called")
    return await service.create_product(product)
