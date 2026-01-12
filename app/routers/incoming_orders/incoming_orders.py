import logging
from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schemas import (
    IncomingOrderCreate,
    IncomingOrderResponse,
    IncomingOrderSummary,
    User,
    IncomingOrderStatusUpdate,
)
from app.db.database import get_db
from app.db.models import UserRole
from app.auth.auth_utils import get_current_user, role_required
from app.services.incoming_orders_service import IncomingOrderService

logger = logging.getLogger(__name__)

router = APIRouter()


def get_incoming_order_service(require_user: bool = False):
    if require_user:

        async def _get_service(
            db: AsyncSession = Depends(get_db),
            current_user: User = Depends(get_current_user),
        ):
            return IncomingOrderService(db, current_user)
    else:

        async def _get_service(db: AsyncSession = Depends(get_db)):
            return IncomingOrderService(db, None)

    return _get_service


@router.post(
    "/", response_model=IncomingOrderResponse, status_code=status.HTTP_201_CREATED
)
async def create_incoming_order(
    order: IncomingOrderCreate,
    service: IncomingOrderService = Depends(get_incoming_order_service(True)),
    has_permissions: bool = Depends(role_required([UserRole.admin, UserRole.staff])),
):
    logger.info("create incoming order endpoint called")
    return await service.create_incoming_order(order)


@router.get(
    "/", response_model=List[IncomingOrderSummary], status_code=status.HTTP_200_OK
)
async def get_all_incoming_orders(
    service: IncomingOrderService = Depends(get_incoming_order_service(True)),
    has_permissions: bool = Depends(role_required([UserRole.admin, UserRole.staff])),
):
    logger.info("get all incoming orders endpoint called")
    return await service.get_all_incoming_orders()


@router.get(
    "/{id}", response_model=IncomingOrderResponse, status_code=status.HTTP_200_OK
)
async def get_incoming_order_by_id(
    id: int,
    service: IncomingOrderService = Depends(get_incoming_order_service(True)),
    has_permissions: bool = Depends(role_required([UserRole.admin, UserRole.staff, UserRole.supplier])),
):
    logger.info("get incoming order by id endpoint called")
    return await service.get_incoming_order_by_id(id)

@router.get(
    "/me", response_model=List[IncomingOrderSummary], status_code=status.HTTP_200_OK
)
async def get_my_incoming_orders(
    service: IncomingOrderService = Depends(get_incoming_order_service(True)),
    has_permissions: bool = Depends(role_required([UserRole.supplier])),
):
    logger.info("get my incoming orders endpoint called")
    return await service.get_my_incoming_orders()

@router.patch(
    "/{id}", response_model=IncomingOrderResponse, status_code=status.HTTP_200_OK
)
async def update_incoming_order_status(
    id: int,
    status_update: IncomingOrderStatusUpdate,
    service: IncomingOrderService = Depends(get_incoming_order_service(True)),
    has_permissions: bool = Depends(role_required([UserRole.admin, UserRole.staff, UserRole.supplier])),
):
    logger.info(f"update incoming order status endpoint called for order {id}")
    return await service.update_incoming_order_status(id, status_update)
