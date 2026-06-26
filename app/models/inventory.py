from sqlalchemy import Column, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base

class Warehouse(Base):
    name = Column(String(100), index=True, nullable=False)
    location_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=True)
    manager_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=True)
    
    address = relationship("Address")
    manager = relationship("Employee")
    inventory = relationship("Inventory", back_populates="warehouse")

class Inventory(Base):
    warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    quantity_on_hand = Column(Numeric(10, 2), default=0, nullable=False)
    reorder_level = Column(Numeric(10, 2), default=10, nullable=True)
    
    warehouse = relationship("Warehouse", back_populates="inventory")
    product = relationship("Product")
