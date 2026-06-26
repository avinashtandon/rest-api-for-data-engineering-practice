from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.database.session import get_db
from app.schemas.response import StandardResponse
from app.schemas.people import (
    CustomerCreate, CustomerUpdate, CustomerResponse,
    SupplierCreate, SupplierUpdate, SupplierResponse,
    EmployeeCreate, EmployeeUpdate, EmployeeResponse
)
from app.services.people import customer_service, supplier_service, employee_service
from app.api.dependencies import get_current_manager, get_current_user

router = APIRouter(prefix="/people", tags=["People"])

# ================= Customers =================

@router.get("/customers", response_model=StandardResponse[List[CustomerResponse]])
async def get_customers(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=1000), 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user)
):
    customers = await customer_service.get_multi(db, skip=skip, limit=limit)
    return StandardResponse(success=True, message="Customers retrieved", data=customers["data"], total_records=customers["total_records"], total_pages=customers["total_pages"], page=customers["page"], limit=customers["limit"])

@router.get("/customers/{id}", response_model=StandardResponse[CustomerResponse])
async def get_customer(id: UUID, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    customer = await customer_service.get(db, id=id)
    return StandardResponse(success=True, message="Customer retrieved", data=customer["data"], total_records=customer["total_records"], total_pages=customer["total_pages"], page=customer["page"], limit=customer["limit"])

@router.post("/customers", response_model=StandardResponse[CustomerResponse])
async def create_customer(
    customer_in: CustomerCreate, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    customer = await customer_service.create(db, obj_in=customer_in)
    return StandardResponse(success=True, message="Customer created", data=customer["data"], total_records=customer["total_records"], total_pages=customer["total_pages"], page=customer["page"], limit=customer["limit"])

@router.put("/customers/{id}", response_model=StandardResponse[CustomerResponse])
async def update_customer(
    id: UUID, 
    customer_in: CustomerUpdate, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    customer = await customer_service.update(db, id=id, obj_in=customer_in)
    return StandardResponse(success=True, message="Customer updated", data=customer["data"], total_records=customer["total_records"], total_pages=customer["total_pages"], page=customer["page"], limit=customer["limit"])

@router.delete("/customers/{id}", response_model=StandardResponse[CustomerResponse])
async def delete_customer(
    id: UUID, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    customer = await customer_service.remove(db, id=id)
    return StandardResponse(success=True, message="Customer deleted", data=customer["data"], total_records=customer["total_records"], total_pages=customer["total_pages"], page=customer["page"], limit=customer["limit"])

# ================= Suppliers =================

@router.get("/suppliers", response_model=StandardResponse[List[SupplierResponse]])
async def get_suppliers(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=1000), 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user)
):
    suppliers = await supplier_service.get_multi(db, skip=skip, limit=limit)
    return StandardResponse(success=True, message="Suppliers retrieved", data=suppliers["data"], total_records=suppliers["total_records"], total_pages=suppliers["total_pages"], page=suppliers["page"], limit=suppliers["limit"])

@router.get("/suppliers/{id}", response_model=StandardResponse[SupplierResponse])
async def get_supplier(id: UUID, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    supplier = await supplier_service.get(db, id=id)
    return StandardResponse(success=True, message="Supplier retrieved", data=supplier["data"], total_records=supplier["total_records"], total_pages=supplier["total_pages"], page=supplier["page"], limit=supplier["limit"])

@router.post("/suppliers", response_model=StandardResponse[SupplierResponse])
async def create_supplier(
    supplier_in: SupplierCreate, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    supplier = await supplier_service.create(db, obj_in=supplier_in)
    return StandardResponse(success=True, message="Supplier created", data=supplier["data"], total_records=supplier["total_records"], total_pages=supplier["total_pages"], page=supplier["page"], limit=supplier["limit"])

@router.put("/suppliers/{id}", response_model=StandardResponse[SupplierResponse])
async def update_supplier(
    id: UUID, 
    supplier_in: SupplierUpdate, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    supplier = await supplier_service.update(db, id=id, obj_in=supplier_in)
    return StandardResponse(success=True, message="Supplier updated", data=supplier["data"], total_records=supplier["total_records"], total_pages=supplier["total_pages"], page=supplier["page"], limit=supplier["limit"])

@router.delete("/suppliers/{id}", response_model=StandardResponse[SupplierResponse])
async def delete_supplier(
    id: UUID, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    supplier = await supplier_service.remove(db, id=id)
    return StandardResponse(success=True, message="Supplier deleted", data=supplier["data"], total_records=supplier["total_records"], total_pages=supplier["total_pages"], page=supplier["page"], limit=supplier["limit"])

# ================= Employees =================

@router.get("/employees", response_model=StandardResponse[List[EmployeeResponse]])
async def get_employees(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=1000), 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user)
):
    employees = await employee_service.get_multi(db, skip=skip, limit=limit)
    return StandardResponse(success=True, message="Employees retrieved", data=employees["data"], total_records=employees["total_records"], total_pages=employees["total_pages"], page=employees["page"], limit=employees["limit"])

@router.get("/employees/{id}", response_model=StandardResponse[EmployeeResponse])
async def get_employee(id: UUID, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    employee = await employee_service.get(db, id=id)
    return StandardResponse(success=True, message="Employee retrieved", data=employee["data"], total_records=employee["total_records"], total_pages=employee["total_pages"], page=employee["page"], limit=employee["limit"])

@router.post("/employees", response_model=StandardResponse[EmployeeResponse])
async def create_employee(
    employee_in: EmployeeCreate, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    employee = await employee_service.create(db, obj_in=employee_in)
    return StandardResponse(success=True, message="Employee created", data=employee["data"], total_records=employee["total_records"], total_pages=employee["total_pages"], page=employee["page"], limit=employee["limit"])

@router.put("/employees/{id}", response_model=StandardResponse[EmployeeResponse])
async def update_employee(
    id: UUID, 
    employee_in: EmployeeUpdate, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    employee = await employee_service.update(db, id=id, obj_in=employee_in)
    return StandardResponse(success=True, message="Employee updated", data=employee["data"], total_records=employee["total_records"], total_pages=employee["total_pages"], page=employee["page"], limit=employee["limit"])

@router.delete("/employees/{id}", response_model=StandardResponse[EmployeeResponse])
async def delete_employee(
    id: UUID, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    employee = await employee_service.remove(db, id=id)
    return StandardResponse(success=True, message="Employee deleted", data=employee["data"], total_records=employee["total_records"], total_pages=employee["total_pages"], page=employee["page"], limit=employee["limit"])
