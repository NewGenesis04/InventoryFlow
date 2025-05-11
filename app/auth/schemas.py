from pydantic import BaseModel
from pydantic import EmailStr, field_validator
from typing import List, Optional
from datetime import datetime
from pydantic import ConfigDict 

class BaseAuth(BaseModel):
    email: EmailStr
    password: str    
    class Config:
        model_config = ConfigDict(from_attributes=True)  # Enables ORM mode

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

