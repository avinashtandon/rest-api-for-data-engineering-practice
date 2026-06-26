from sqlalchemy import Column, String, Text, ForeignKey, Numeric, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base

class Category(Base):
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Relationships
    products = relationship("Product", back_populates="category")

class Product(Base):
    name = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=True)
    sku = Column(String(50), unique=True, index=True, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    weight = Column(Numeric(10, 2), nullable=True)
    dimensions = Column(String(100), nullable=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categorys.id"), nullable=True)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"), nullable=True)
    
    # Relationships
    category = relationship("Category", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")
