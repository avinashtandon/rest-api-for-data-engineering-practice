from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

from app.models.user import RoleEnum

class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role: RoleEnum = RoleEnum.VIEWER

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None
    is_locked: Optional[bool] = None

class UserResponse(UserBase):
    id: UUID
    role: RoleEnum
    is_active: bool
    is_locked: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
