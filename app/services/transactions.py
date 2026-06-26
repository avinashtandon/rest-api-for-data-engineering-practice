from app.services.base import BaseService
from app.models.transactions import Order, OrderItem, Payment, Invoice, Shipment
from app.schemas.transactions import (
    OrderCreate, OrderUpdate,
    OrderItemCreate, OrderItemUpdate,
    PaymentCreate, PaymentUpdate,
    InvoiceCreate, InvoiceUpdate,
    ShipmentCreate, ShipmentUpdate
)
from app.repositories.transactions import (
    order_repo, order_item_repo, payment_repo, invoice_repo, shipment_repo
)

class OrderService(BaseService[Order, OrderCreate, OrderUpdate]):
    pass

class OrderItemService(BaseService[OrderItem, OrderItemCreate, OrderItemUpdate]):
    pass

class PaymentService(BaseService[Payment, PaymentCreate, PaymentUpdate]):
    pass

class InvoiceService(BaseService[Invoice, InvoiceCreate, InvoiceUpdate]):
    pass

class ShipmentService(BaseService[Shipment, ShipmentCreate, ShipmentUpdate]):
    pass

order_service = OrderService(order_repo)
order_item_service = OrderItemService(order_item_repo)
payment_service = PaymentService(payment_repo)
invoice_service = InvoiceService(invoice_repo)
shipment_service = ShipmentService(shipment_repo)
