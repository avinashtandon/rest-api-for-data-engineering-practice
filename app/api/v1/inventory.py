from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.database.session import get_db
from app.schemas.response import StandardResponse
from app.schemas.inventory import (
    WarehouseCreate, WarehouseUpdate, WarehouseResponse,
    InventoryCreate, InventoryUpdate, InventoryResponse
)
from app.services.inventory import warehouse_service, inventory_service
from app.api.dependencies import get_current_manager, get_current_user

router = APIRouter(prefix="/inventory", tags=["Inventory"])

# ================= Warehouses =================

@router.get("/warehouses", response_model=StandardResponse[List[WarehouseResponse]])
async def get_warehouses(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=1000), 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user)
):
    warehouses = await warehouse_service.get_multi(db, skip=skip, limit=limit)
    return StandardResponse(success=True, message="Warehouses retrieved", data=warehouses["data"], total_records=warehouses["total_records"], total_pages=warehouses["total_pages"], page=warehouses["page"], limit=warehouses["limit"])

@router.post("/warehouses", response_model=StandardResponse[WarehouseResponse])
async def create_warehouse(
    warehouse_in: WarehouseCreate, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    warehouse = await warehouse_service.create(db, obj_in=warehouse_in)
    return StandardResponse(success=True, message="Warehouse created", data=warehouse["data"], total_records=warehouse["total_records"], total_pages=warehouse["total_pages"], page=warehouse["page"], limit=warehouse["limit"])

# ================= Inventory =================

@router.get("/items", response_model=StandardResponse[List[InventoryResponse]])
async def get_inventory_items(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=1000), 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user)
):
    inventory = await inventory_service.get_multi(db, skip=skip, limit=limit)
    return StandardResponse(success=True, message="Inventory retrieved", data=inventory["data"], total_records=inventory["total_records"], total_pages=inventory["total_pages"], page=inventory["page"], limit=inventory["limit"])
