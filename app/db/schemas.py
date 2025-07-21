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
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    address: Optional[str]

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
    name: Optional[str]
    phone_number: Optional[str]
    email: Optional[EmailStr]
    address: Optional[str]

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
    quantity: Optional[int]
    category_id: int

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[int]
    quantity: Optional[int]
    category_id: Optional[int]

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
    quantity: Optional[int]
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
    name: Optional[str]
    description: Optional[str]

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StockCreate(BaseModel):
    product_id: int
    available_quantity: int
    product_price: Optional[int]
    total_price: Optional[int]

class StockUpdate(BaseModel):
    available_quantity: Optional[int]
    product_price: Optional[int]
    total_price: Optional[int]


class StockResponse(BaseModel):
    id: int
    product: ProductSummary
    available_quantity: int
    product_price: Optional[int]
    total_price: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


#  IncomingOrder Schemas
class IncomingOrderBase(BaseModel):
    quantity: int
    total_price: int
    supply_date: datetime

    class Config:
        from_attributes = True
        
class IncomingOrderCreate(IncomingOrderBase):
    supplier_id: int
    product_id: int

class IncomingOrderResponse(IncomingOrderBase):
    id: int
    supplier: SupplierSummary
    product: ProductSummary
    created_at: datetime
    updated_at: datetime

#  OutgoingOrder Schemas

class OutgoingOrderBase(BaseModel):
    quantity: int
    total_price: int
    order_date: datetime

    class Config:
        from_attributes = True
class OutgoingOrderCreate(OutgoingOrderBase):
    customer_id: int
    product_id: int

class OutgoingOrderResponse(OutgoingOrderBase):
    id: int
    customer: CustomerSummary
    product: ProductSummary
    created_at: datetime
    updated_at: datetime

class OrderStatusUpdate(BaseModel):
    status: str  # e.g., "completed" or "cancelled"