from sqlalchemy.ext.asyncio import AsyncSession
from app.services.base import BaseService
from app.db.models import Supplier, UserRole
from app.db.schemas import SupplierCreate, SupplierUpdate, PaginatedResponse, SupplierSummary
from sqlalchemy.future import select
from fastapi import HTTPException, status
from typing import List, Optional
from app.utils import paginate

class SupplierService(BaseService):
    async def create_supplier(self, supplier_data: SupplierCreate) -> Supplier:
        supplier = Supplier(**supplier_data.model_dump())
        self.db.add(supplier)
        await self.db.commit()
        await self.db.refresh(supplier)
        return supplier

    async def get_all_suppliers(self, limit: int, after: Optional[str] = None, before: Optional[str] = None) -> PaginatedResponse[SupplierSummary]:
        paginated_suppliers = await paginate(
            db=self.db,
            model=Supplier,
            limit=limit,
            after=after,
            before=before
        )
        if not paginated_suppliers.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No suppliers found")
        return paginated_suppliers

    async def get_supplier_by_id(self, supplier_id: int) -> Supplier:
        supplier = await self.db.get(Supplier, supplier_id)
        if not supplier:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
        return supplier

    async def get_my_supplier_profile(self) -> Supplier:
        result = await self.db.execute(select(Supplier).where(Supplier.user_id == self.user.id))
        supplier = result.scalars().first()
        if not supplier:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier profile not found for current user")
        return supplier

    async def update_supplier(self, supplier_id: int, supplier_data: SupplierUpdate) -> Supplier:
        supplier = await self.db.get(Supplier, supplier_id)
        if not supplier:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")

        update_data = supplier_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(supplier, key, value)
        
        await self.db.commit()
        await self.db.refresh(supplier)
        return supplier

    async def delete_supplier(self, supplier_id: int) -> None:
        supplier = await self.db.get(Supplier, supplier_id)
        if not supplier:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")

        await self.db.delete(supplier)
        await self.db.commit()
        return
