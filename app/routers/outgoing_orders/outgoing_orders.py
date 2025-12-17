import logging
from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schemas import OutgoingOrderCreate, OutgoingOrderResponse, OutgoingOrderSummary, User
from app.db.database import get_db
from app.db.models import UserRole
from app.auth.auth_utils import get_current_user, role_required
from app.services import OutgoingOrderService

logger = logging.getLogger(__name__)

router = APIRouter()

def get_outgoing_order_service(require_user: bool = False):
    if require_user:
        async def _get_service(
            db: AsyncSession = Depends(get_db),
            current_user: User = Depends(get_current_user),
        ):
            return OutgoingOrderService(db, current_user)
    else:
        async def _get_service(db: AsyncSession = Depends(get_db)):
            return OutgoingOrderService(db, None)
    
    return _get_service

@router.post("/", response_model=OutgoingOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_outgoing_order(order: OutgoingOrderCreate, service: OutgoingOrderService = Depends(get_outgoing_order_service(True)), has_permissions: bool = Depends(role_required([UserRole.admin]))):
    logger.info("create outgoing order endpoint called")
    return await service.create_outgoing_order(order)

@router.get("/", response_model=List[OutgoingOrderSummary], status_code=status.HTTP_200_OK)
async def get_all_outgoing_orders(service: OutgoingOrderService = Depends(get_outgoing_order_service(True))):
    logger.info("get all outgoing orders endpoint called")
    return await service.get_all_outgoing_orders()

@router.get("/{id}", response_model=OutgoingOrderResponse, status_code=status.HTTP_200_OK)
async def get_outgoing_order_by_id(id: int, service: OutgoingOrderService = Depends(get_outgoing_order_service(True))):
    logger.info("get outgoing order by id endpoint called")
    return await service.get_outgoing_order_by_id(id)
