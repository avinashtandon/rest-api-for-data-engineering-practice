from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class OrderBase(BaseModel):
    customer_id: UUID
    order_date: datetime
    status: str = "Pending"
    total_amount: float
    shipping_address_id: Optional[UUID] = None
    billing_address_id: Optional[UUID] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    total_amount: Optional[float] = None
    shipping_address_id: Optional[UUID] = None
    billing_address_id: Optional[UUID] = None
    is_active: Optional[bool] = None

class OrderResponse(OrderBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class OrderItemBase(BaseModel):
    order_id: UUID
    product_id: UUID
    quantity: float
    unit_price: float
    discount: Optional[float] = 0

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    discount: Optional[float] = None
    is_active: Optional[bool] = None

class OrderItemResponse(OrderItemBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PaymentBase(BaseModel):
    order_id: UUID
    payment_date: datetime
    amount: float
    payment_method: str
    status: str = "Completed"
    transaction_id: Optional[str] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    status: Optional[str] = None
    is_active: Optional[bool] = None

class PaymentResponse(PaymentBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class InvoiceBase(BaseModel):
    order_id: UUID
    invoice_date: datetime
    due_date: Optional[datetime] = None
    total_amount: float
    status: str = "Issued"

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(BaseModel):
    due_date: Optional[datetime] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None

class InvoiceResponse(InvoiceBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ShipmentBase(BaseModel):
    order_id: UUID
    shipment_date: Optional[datetime] = None
    carrier: Optional[str] = None
    tracking_number: Optional[str] = None
    status: str = "Processing"

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentUpdate(BaseModel):
    shipment_date: Optional[datetime] = None
    carrier: Optional[str] = None
    tracking_number: Optional[str] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None

class ShipmentResponse(ShipmentBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
