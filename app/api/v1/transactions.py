from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.database.session import get_db
from app.schemas.response import StandardResponse
from app.schemas.transactions import (
    OrderCreate, OrderUpdate, OrderResponse,
    PaymentCreate, PaymentUpdate, PaymentResponse,
    InvoiceCreate, InvoiceUpdate, InvoiceResponse,
    ShipmentCreate, ShipmentUpdate, ShipmentResponse
)
from app.services.transactions import (
    order_service, payment_service, invoice_service, shipment_service
)
from app.api.dependencies import get_current_manager, get_current_user, get_query_params

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# ================= Orders =================

@router.get("/orders", response_model=StandardResponse[List[OrderResponse]])
async def get_orders(
    query_params: dict = Depends(get_query_params),
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user)
):
    result = await order_service.get_multi(db, **query_params)
    return StandardResponse(
        success=True, 
        message="Orders retrieved", 
        data=result["data"],
        total_records=result["total_records"],
        total_pages=result["total_pages"],
        page=result["page"],
        limit=result["limit"],
        next_page=result["next_page"],
        previous_page=result["previous_page"]
    )

@router.get("/orders/{id}", response_model=StandardResponse[OrderResponse])
async def get_order(id: UUID, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    order = await order_service.get(db, id=id)
    return StandardResponse(success=True, message="Order retrieved", data=order["data"], total_records=order["total_records"], total_pages=order["total_pages"], page=order["page"], limit=order["limit"])

@router.post("/orders", response_model=StandardResponse[OrderResponse])
async def create_order(
    order_in: OrderCreate, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    order = await order_service.create(db, obj_in=order_in)
    return StandardResponse(success=True, message="Order created", data=order["data"], total_records=order["total_records"], total_pages=order["total_pages"], page=order["page"], limit=order["limit"])

# ================= Payments =================

@router.get("/payments", response_model=StandardResponse[List[PaymentResponse]])
async def get_payments(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=1000), 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user)
):
    payments = await payment_service.get_multi(db, skip=skip, limit=limit)
    return StandardResponse(success=True, message="Payments retrieved", data=payments["data"], total_records=payments["total_records"], total_pages=payments["total_pages"], page=payments["page"], limit=payments["limit"])

@router.post("/payments", response_model=StandardResponse[PaymentResponse])
async def create_payment(
    payment_in: PaymentCreate, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    payment = await payment_service.create(db, obj_in=payment_in)
    return StandardResponse(success=True, message="Payment created", data=payment["data"], total_records=payment["total_records"], total_pages=payment["total_pages"], page=payment["page"], limit=payment["limit"])

# ================= Invoices =================

@router.get("/invoices", response_model=StandardResponse[List[InvoiceResponse]])
async def get_invoices(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=1000), 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user)
):
    invoices = await invoice_service.get_multi(db, skip=skip, limit=limit)
    return StandardResponse(success=True, message="Invoices retrieved", data=invoices["data"], total_records=invoices["total_records"], total_pages=invoices["total_pages"], page=invoices["page"], limit=invoices["limit"])

# ================= Shipments =================

@router.get("/shipments", response_model=StandardResponse[List[ShipmentResponse]])
async def get_shipments(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=1000), 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user)
):
    shipments = await shipment_service.get_multi(db, skip=skip, limit=limit)
    return StandardResponse(success=True, message="Shipments retrieved", data=shipments["data"], total_records=shipments["total_records"], total_pages=shipments["total_pages"], page=shipments["page"], limit=shipments["limit"])
