from sqlalchemy import Column, String, Boolean, Enum as SAEnum
from typing import Optional
import enum

from app.models.base import Base

class RoleEnum(str, enum.Enum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    DATA_ENGINEER = "DataEngineer"
    ANALYST = "Analyst"
    VIEWER = "Viewer"

class User(Base):
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    phone_number = Column(String(50), nullable=True)
    role = Column(SAEnum(RoleEnum), default=RoleEnum.VIEWER, nullable=False)
    is_locked = Column(Boolean, default=False, nullable=False)
    refresh_token = Column(String, nullable=True)  # Store current valid refresh token
