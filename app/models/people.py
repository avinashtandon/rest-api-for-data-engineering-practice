from sqlalchemy import Column, String, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base

class Customer(Base):
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(50), nullable=True)
    loyalty_tier = Column(String(50), default="Bronze")

class Supplier(Base):
    name = Column(String(255), index=True, nullable=False)
    contact_name = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    tax_id = Column(String(100), nullable=True)
    
    products = relationship("Product", back_populates="supplier")

class Employee(Base):
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(50), nullable=True)
    job_title = Column(String(100), nullable=True)
    hire_date = Column(Date, nullable=True)
    salary = Column(Numeric(12, 2), nullable=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    
    department = relationship("Department", back_populates="employees")
