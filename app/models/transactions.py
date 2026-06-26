from sqlalchemy import Column, String, ForeignKey, Numeric, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base

class Order(Base):
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    order_date = Column(DateTime, nullable=False)
    status = Column(String(50), default="Pending", nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    shipping_address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=True)
    billing_address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=True)
    
    # Relationships
    customer = relationship("Customer")
    items = relationship("OrderItem", back_populates="order")
    payments = relationship("Payment", back_populates="order")
    invoices = relationship("Invoice", back_populates="order")
    shipments = relationship("Shipment", back_populates="order")

class OrderItem(Base):
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    discount = Column(Numeric(12, 2), default=0)
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product")

class Payment(Base):
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    payment_date = Column(DateTime, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    payment_method = Column(String(50), nullable=False)
    status = Column(String(50), default="Completed", nullable=False)
    transaction_id = Column(String(100), nullable=True)
    
    order = relationship("Order", back_populates="payments")

class Invoice(Base):
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    invoice_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=True)
    total_amount = Column(Numeric(12, 2), nullable=False)
    status = Column(String(50), default="Issued", nullable=False)
    
    order = relationship("Order", back_populates="invoices")

class Shipment(Base):
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    shipment_date = Column(DateTime, nullable=True)
    carrier = Column(String(100), nullable=True)
    tracking_number = Column(String(100), nullable=True)
    status = Column(String(50), default="Processing", nullable=False)
    
    order = relationship("Order", back_populates="shipments")
    tracking_events = relationship("ShipmentTracking", back_populates="shipment")

class ShipmentTracking(Base):
    shipment_id = Column(UUID(as_uuid=True), ForeignKey("shipments.id"), nullable=False)
    event_date = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    
    shipment = relationship("Shipment", back_populates="tracking_events")
