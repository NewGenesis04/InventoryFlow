from pydantic import BaseModel
from pydantic import EmailStr
from app.db.models import UserRole
from typing import List, Optional, Literal
from datetime import datetime
from pydantic import ConfigDict 

class BaseAuth(BaseModel):
    email: EmailStr
    password: str    
    class Config:
        from_attributes = True

class AuthLogin(BaseAuth):
    pass

class AuthRegister(BaseAuth):
    username: str
    first_name: str
    last_name: str
    role: UserRole
    phone: Optional[str] = None
    address: Optional[str] = None

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class AuthPasswordUpdate(BaseModel):
    old_password: str
    new_password: str

class User(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    role: str
    email: str

    class Config:
        from_attributes = True


# Customer Schemas
class CustomerCreate(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    phone_number: Optional[str]
    address: Optional[str]

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class CustomerResponse(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    phone_number: Optional[str]
    address: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CustomerSummary(BaseModel):
    id: int
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

# Supplier Schemas
class SupplierCreate(BaseModel):
    user_id: int
    name: str
    phone_number: Optional[str]
    email: Optional[EmailStr]
    address: Optional[str]

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None

class SupplierResponse(BaseModel):
    id: int
    user_id: int
    name: str
    phone_number: Optional[str]
    email: Optional[EmailStr]
    address: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SupplierSummary(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# Product Schemas
class ProductCreate(BaseModel):
    name: str
    description: Optional[str]
    price: Optional[int]
    category_id: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    category_id: Optional[int] = None

class ProductCategorySummary(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: Optional[int]
    category: ProductCategorySummary
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProductSummary(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# Category Schemas
class CategoryCreate(BaseModel):
    name: str
    description: Optional[str]

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StockUpdate(BaseModel):
    available_quantity: Optional[int] = None

class StockResponse(BaseModel):
    id: int
    product: ProductSummary
    batch_number: Optional[str]
    available_quantity: int
    expiry_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StockSummary(BaseModel):
    id: int
    available_quantity: int

    class Config:
        from_attributes = True


#  IncomingOrder Schemas

class IncomingOrderCreate(BaseModel):
    supplier_id: int
    product_id: int
    batch_number: str
    quantity: int
    unit_cost: float
    supply_date: datetime
    expiry_date: Optional[datetime] = None

class IncomingOrderResponse(BaseModel):
    id: int
    supplier: SupplierSummary
    product: ProductSummary
    batch_number: str
    quantity: int
    unit_cost: float
    total_cost: float
    status: str
    supply_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class IncomingOrderSummary(BaseModel):
    id: int
    supplier_id: int
    product_id: int
    batch_number: str
    quantity: int
    total_cost: float
    status: str
    supply_date: datetime

    class Config:
        from_attributes = True

#  OutgoingOrder Schemas

class OutgoingOrderCreate(BaseModel):
    customer_id: int
    product_id: int
    stock_id: int
    quantity: int
    order_date: datetime

class OutgoingOrderResponse(BaseModel):
    id: int
    customer: CustomerSummary
    product: ProductSummary
    quantity: int
    unit_price: Optional[int]
    total_price: int
    status: str
    order_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class OutgoingOrderSummary(BaseModel):
    id: int
    customer_id: int
    product_id: int
    quantity: int
    total_price: int
    status: str
    order_date: datetime

    class Config:
        from_attributes = True
