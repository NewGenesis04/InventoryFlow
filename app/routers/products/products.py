import logging
from fastapi import APIRouter, Depends, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schemas import ProductCreate, ProductResponse, User, ProductUpdate, ProductSummary, PaginatedResponse
from app.db.database import get_db
from app.db.models import UserRole
from app.auth.auth_utils import get_current_user, role_required
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

@router.post("/create", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, service: ProductService = Depends(get_product_service(True)), has_permissions: bool = Depends(role_required([UserRole.admin]))):
    logger.info("create_product endpoint called")
    return await service.create_product(product)

@router.get("/{id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def get_product_by_id(id: int, service: ProductService = Depends(get_product_service(True)), has_permissions: bool = Depends(role_required([UserRole.admin, UserRole.staff, UserRole.customer, UserRole.supplier]))):
    logger.info("get product by id endpoint called")
    return await service.get_product_by_id(id)

@router.get("/", response_model=PaginatedResponse[ProductSummary], status_code=status.HTTP_200_OK)
async def get_all_products(
    limit: int = 10,
    after: Optional[str] = None,
    before: Optional[str] = None,
    service: ProductService = Depends(get_product_service(True)), 
    has_permissions: bool = Depends(role_required([UserRole.admin, UserRole.staff, UserRole.customer, UserRole.supplier]))
):
    logger.info("get all products endpoint called")
    return await service.get_all_products(limit=limit, after=after, before=before)

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_product(id: int, product_update: ProductUpdate, service: ProductService = Depends(get_product_service(True)), has_permissions: bool = Depends(role_required([UserRole.admin]))):
    logger.info(f"update product endpoint called on ID: {id}")
    return await service.update_product(id, product_update)

@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_product(id: int, service: ProductService = Depends(get_product_service(True)), has_permissions: bool = Depends(role_required([UserRole.admin]))):
    logger.info(f"delete endpoint called on ID: {id}")
    return await service.delete_product(id)
