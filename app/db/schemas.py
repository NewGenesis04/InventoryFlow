from pydantic import BaseModel
from pydantic import EmailStr, field_validator
from typing import List, Optional
from datetime import datetime

class BaseAuth(BaseModel):
    email: EmailStr
    password: str    

class AuthLogin(BaseAuth):
    pass

class AuthRegister(BaseAuth):
    first_name: str
    last_name: str
    role: str
    phone: Optional[str] = None
    address: Optional[str] = None

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class AuthPasswordUpdate(BaseModel):
    old_password: str
    new_password: str

# ==== Product ====
class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: int
    quantity: int
    category_id: int

class ProductOut(ProductCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True

# ==== Stock ====
class StockUpdate(BaseModel):
    quantity: int

class StockOut(BaseModel):
    id: int
    product_id: int
    available_quantity: int
    product_price: int | None = None
    total_price: int
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True

# ==== Incoming Order ====
class IncomingOrderCreate(BaseModel):
    supplier_id: int
    product_id: int
    quantity: int
    supply_date: datetime

class IncomingOrderOut(IncomingOrderCreate):
    id: int
    total_price: int
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True

# ==== Outgoing Order ====
class OutgoingOrderCreate(BaseModel):
    customer_id: int
    product_id: int
    quantity: int
    order_date: datetime

class OutgoingOrderOut(OutgoingOrderCreate):
    id: int
    total_price: int
    created_at: datetime
    updated_at: datetime
