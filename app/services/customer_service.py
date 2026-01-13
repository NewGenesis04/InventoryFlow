from app.services.base import BaseService
from app.db.models import Customer, UserRole
from app.db.schemas import CustomerCreate, CustomerUpdate, PaginatedResponse, CustomerSummary
from fastapi import HTTPException, status
from typing import Optional
from app.utils import paginate

class CustomerService(BaseService):
    async def create_customer(self, customer_data: CustomerCreate) -> Customer:
        customer = Customer(**customer_data.model_dump())
        self.db.add(customer)
        await self.db.commit()
        await self.db.refresh(customer)
        return customer

    async def get_all_customers(self, limit: int, after: Optional[str] = None, before: Optional[str] = None) -> PaginatedResponse[CustomerSummary]:
        paginated_customers = await paginate(
            db=self.db,
            model=Customer,
            limit=limit,
            after=after,
            before=before
        )
        if not paginated_customers.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No customers found")
        return paginated_customers

    async def get_customer_by_id(self, customer_id: int) -> Customer:
        customer = await self.db.get(Customer, customer_id)
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        
        # Admin and staff can see any customer
        if self.user.role in [UserRole.admin, UserRole.staff]:
            return customer
        
        # A customer can only see their own profile
        if self.user.id != customer.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this customer")
            
        return customer

    async def update_customer(self, customer_id: int, customer_data: CustomerUpdate) -> Customer:
        customer = await self.db.get(Customer, customer_id)
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

        update_data = customer_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(customer, key, value)
        
        await self.db.commit()
        await self.db.refresh(customer)
        return customer

    async def delete_customer(self, customer_id: int) -> None:
        customer = await self.db.get(Customer, customer_id)
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

        await self.db.delete(customer)
        await self.db.commit()
        return
