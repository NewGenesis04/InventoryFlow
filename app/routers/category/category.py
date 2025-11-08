from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schemas import User
from app.db.database import get_db
from app.db.schemas import CategoryCreate, CategoryResponse, CategoryUpdate
from typing import List
from app.auth.auth_utils import get_current_user, role_required
from app.db.models import UserRole
from app.services import CategoryService
import logging

logger = logging.getLogger(__name__)

def get_category_service(require_user: bool = False):
    if require_user:
        async def _get_service(
            db: AsyncSession = Depends(get_db),
            current_user: User = Depends(get_current_user),
        ):
            return CategoryService(db, current_user)
    else:
        async def _get_service(db: AsyncSession = Depends(get_db)):
            return CategoryService(db, None)
    
    return _get_service

router = APIRouter()

@router.post("/create", response_model=CategoryResponse, status_code=201)
async def create_category(category: CategoryCreate, service: CategoryService = Depends(get_category_service(True)), has_permission: bool = Depends(role_required([UserRole.admin]))):
    logger.info("create_category endpoint called")
    return await service.create_category(category)

@router.get("/{category_id}", response_model=CategoryResponse, status_code=200)
async def get_category_by_id(category_id: int, service: CategoryService = Depends(get_category_service(False))):
    logger.info(f"get_category endpoint called for ID: {category_id}")
    return await service.get_category_by_id(category_id)

@router.get("/", response_model=List[CategoryResponse], status_code=200)
async def get_all_categories(service: CategoryService = Depends(get_category_service(False))):
    logger.info("get_all_categories endpoint called")
    return await service.get_all_categories()

@router.put("/{category_id}", response_model=CategoryResponse, status_code=200)
async def update_category(category_id: int, category_data: CategoryUpdate, service: CategoryService = Depends(get_category_service(True)), has_permission: bool = Depends(role_required([UserRole.admin]))):
    logger.info(f"update_category endpoint called for ID: {category_id}")
    return await service.update_category(category_id, category_data)

@router.delete("/{category_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_category(category_id: int, service: CategoryService = Depends(get_category_service(True)), has_permission: bool = Depends(role_required([UserRole.admin]))) :
    logger.info(f"delete endpoint called for ID: {category_id}")
