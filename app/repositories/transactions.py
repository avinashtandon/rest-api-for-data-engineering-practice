from app.repositories.base import BaseRepository
from app.models.transactions import Order, OrderItem, Payment, Invoice, Shipment
from app.schemas.transactions import (
    OrderCreate, OrderUpdate,
    OrderItemCreate, OrderItemUpdate,
    PaymentCreate, PaymentUpdate,
    InvoiceCreate, InvoiceUpdate,
    ShipmentCreate, ShipmentUpdate
)

class OrderRepository(BaseRepository[Order, OrderCreate, OrderUpdate]):
    pass

class OrderItemRepository(BaseRepository[OrderItem, OrderItemCreate, OrderItemUpdate]):
    pass

class PaymentRepository(BaseRepository[Payment, PaymentCreate, PaymentUpdate]):
    pass

class InvoiceRepository(BaseRepository[Invoice, InvoiceCreate, InvoiceUpdate]):
    pass

class ShipmentRepository(BaseRepository[Shipment, ShipmentCreate, ShipmentUpdate]):
    pass

order_repo = OrderRepository(Order)
order_item_repo = OrderItemRepository(OrderItem)
payment_repo = PaymentRepository(Payment)
invoice_repo = InvoiceRepository(Invoice)
shipment_repo = ShipmentRepository(Shipment)
