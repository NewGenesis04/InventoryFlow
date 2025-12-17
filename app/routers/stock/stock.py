import logging
from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schemas import StockUpdate, StockResponse, StockSummary, User
from app.db.database import get_db
from app.db.models import UserRole
from app.auth.auth_utils import get_current_user, role_required
from app.services import StockService

logger = logging.getLogger(__name__)

router = APIRouter()

def get_stock_service(require_user: bool = False):
    if require_user:
        async def _get_service(
            db: AsyncSession = Depends(get_db),
            current_user: User = Depends(get_current_user),
        ):
            return StockService(db, current_user)
    else:
        async def _get_service(db: AsyncSession = Depends(get_db)):
            return StockService(db, None)
    
    return _get_service

@router.get("/", response_model=List[StockSummary], status_code=status.HTTP_200_OK)
async def get_all_stocks(service: StockService = Depends(get_stock_service(True))):
    logger.info("get all stocks endpoint called")
    return await service.get_all_stocks()

@router.get("/{id}", response_model=StockResponse, status_code=status.HTTP_200_OK)
async def get_stock_by_id(id: int, service: StockService = Depends(get_stock_service(True))):
    logger.info("get stock by id endpoint called")
    return await service.get_stock_by_id(id)

@router.patch("/{id}", response_model=StockResponse, status_code=status.HTTP_200_OK)
async def update_stock(id: int, stock_update: StockUpdate, service: StockService = Depends(get_stock_service(True)), has_permissions: bool = Depends(role_required([UserRole.admin]))):
    logger.info(f"update stock endpoint called on ID: {id}")
    return await service.update_stock(id, stock_update)

