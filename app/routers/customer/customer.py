from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schemas import User
from app.db.database import get_db
from app.db.schemas import CustomerCreate, CustomerResponse, CustomerUpdate, CustomerSummary, PaginatedResponse
from typing import Optional
from app.auth.auth_utils import get_current_user, role_required
from app.db.models import UserRole
from app.services.customer_service import CustomerService
import logging

logger = logging.getLogger(__name__)

def get_customer_service(require_user: bool = False):
    if require_user:
        async def _get_service(
            db: AsyncSession = Depends(get_db),
            current_user: User = Depends(get_current_user),
        ):
            return CustomerService(db, current_user)
    else:
        async def _get_service(db: AsyncSession = Depends(get_db)):
            return CustomerService(db, None)
    
    return _get_service

router = APIRouter()

@router.post("/", response_model=CustomerResponse, status_code=201)
async def create_customer(customer: CustomerCreate, service: CustomerService = Depends(get_customer_service(True)), has_permission: bool = Depends(role_required([UserRole.admin]))):
    logger.info("create_customer endpoint called")
    return await service.create_customer(customer)

@router.get("/", response_model=PaginatedResponse[CustomerSummary], status_code=200)
async def get_all_customers(
    limit: int = 10,
    after: Optional[str] = None,
    before: Optional[str] = None,
    service: CustomerService = Depends(get_customer_service(True)), 
    has_permission: bool = Depends(role_required([UserRole.admin, UserRole.staff]))
):
    logger.info("get_all_customers endpoint called")
    return await service.get_all_customers(limit=limit, after=after, before=before)

@router.get("/{customer_id}", response_model=CustomerResponse, status_code=200)
async def get_customer_by_id(customer_id: int, service: CustomerService = Depends(get_customer_service(True)), has_permission: bool = Depends(role_required([UserRole.admin, UserRole.staff, UserRole.customer]))):
    logger.info(f"get_customer endpoint called for ID: {customer_id}")
    return await service.get_customer_by_id(customer_id)

@router.put("/{customer_id}", response_model=CustomerResponse, status_code=200)
async def update_customer(customer_id: int, customer_data: CustomerUpdate, service: CustomerService = Depends(get_customer_service(True)), has_permission: bool = Depends(role_required([UserRole.admin]))):
    logger.info(f"update_customer endpoint called for ID: {customer_id}")
    return await service.update_customer(customer_id, customer_data)

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: int, service: CustomerService = Depends(get_customer_service(True)), has_permission: bool = Depends(role_required([UserRole.admin]))) :
    logger.info(f"delete endpoint called for ID: {customer_id}")
    await service.delete_customer(customer_id)
    return
