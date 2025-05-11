from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


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
        orm_mode = True


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
        orm_mode = True



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
        orm_mode = True

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
        orm_mode = True


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
        orm_mode = True


# 📦 Stock Schemas
class StockCreate(BaseModel):
    product_id: int
    available_quantity: int
    product_price: Optional[int]
    total_price: Optional[int]

class StockUpdate(BaseModel):
    available_quantity: Optional[int]
    product_price: Optional[int]
    total_price: Optional[int]

class ProductSummary(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class StockResponse(BaseModel):
    id: int
    product: ProductSummary
    available_quantity: int
    product_price: Optional[int]
    total_price: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


#  IncomingOrder Schemas
class IncomingOrderCreate(BaseModel):
    supplier_id: int
    product_id: int
    quantity: int
    total_price: int
    supply_date: datetime

class SupplierSummary(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class IncomingOrderResponse(BaseModel):
    id: int
    supplier: SupplierSummary
    product: ProductSummary
    quantity: int
    total_price: int
    supply_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


#  OutgoingOrder Schemas
class OutgoingOrderCreate(BaseModel):
    customer_id: int
    product_id: int
    quantity: int
    total_price: int
    order_date: datetime

class CustomerSummary(BaseModel):
    id: int
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

class OutgoingOrderResponse(BaseModel):
    id: int
    customer: CustomerSummary
    product: ProductSummary
    quantity: int
    total_price: int
    order_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class OrderStatusUpdate(BaseModel):
    status: str  # e.g., "completed" or "cancelled"
