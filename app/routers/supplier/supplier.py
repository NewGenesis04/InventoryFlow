from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schemas import User
from app.db.database import get_db
from app.db.schemas import SupplierCreate, SupplierResponse, SupplierUpdate, SupplierSummary
from typing import List
from app.auth.auth_utils import get_current_user, role_required
from app.db.models import UserRole
from app.services.supplier_service import SupplierService
import logging

logger = logging.getLogger(__name__)

def get_supplier_service(require_user: bool = False):
    if require_user:
        async def _get_service(
            db: AsyncSession = Depends(get_db),
            current_user: User = Depends(get_current_user),
        ):
            return SupplierService(db, current_user)
    else:
        async def _get_service(db: AsyncSession = Depends(get_db)):
            return SupplierService(db, None)
    
    return _get_service

router = APIRouter()

@router.post("/", response_model=SupplierResponse, status_code=201)
async def create_supplier(supplier: SupplierCreate, service: SupplierService = Depends(get_supplier_service(True)), has_permission: bool = Depends(role_required([UserRole.admin]))):
    logger.info("create_supplier endpoint called")
    return await service.create_supplier(supplier)

@router.get("/", response_model=List[SupplierSummary], status_code=200)
async def get_all_suppliers(service: SupplierService = Depends(get_supplier_service(True)), has_permission: bool = Depends(role_required([UserRole.admin, UserRole.staff]))):
    logger.info("get_all_suppliers endpoint called")
    return await service.get_all_suppliers()

@router.get("/me", response_model=SupplierResponse, status_code=200)
async def get_my_supplier_profile(service: SupplierService = Depends(get_supplier_service(True)), has_permission: bool = Depends(role_required([UserRole.supplier]))):
    logger.info("get_my_supplier_profile endpoint called")
    return await service.get_my_supplier_profile()

@router.get("/{supplier_id}", response_model=SupplierResponse, status_code=200)
async def get_supplier_by_id(supplier_id: int, service: SupplierService = Depends(get_supplier_service(True)), has_permission: bool = Depends(role_required([UserRole.admin, UserRole.staff]))):
    logger.info(f"get_supplier endpoint called for ID: {supplier_id}")
    return await service.get_supplier_by_id(supplier_id)

@router.put("/{supplier_id}", response_model=SupplierResponse, status_code=200)
async def update_supplier(supplier_id: int, supplier_data: SupplierUpdate, service: SupplierService = Depends(get_supplier_service(True)), has_permission: bool = Depends(role_required([UserRole.admin]))):
    logger.info(f"update_supplier endpoint called for ID: {supplier_id}")
    return await service.update_supplier(supplier_id, supplier_data)

@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier(supplier_id: int, service: SupplierService = Depends(get_supplier_service(True)), has_permission: bool = Depends(role_required([UserRole.admin]))) :
    logger.info(f"delete endpoint called for ID: {supplier_id}")
    await service.delete_supplier(supplier_id)
    return
