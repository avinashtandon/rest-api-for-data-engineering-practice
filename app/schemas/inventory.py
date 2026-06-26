from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class WarehouseBase(BaseModel):
    name: str
    location_id: Optional[UUID] = None
    manager_id: Optional[UUID] = None

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseUpdate(BaseModel):
    name: Optional[str] = None
    location_id: Optional[UUID] = None
    manager_id: Optional[UUID] = None
    is_active: Optional[bool] = None

class WarehouseResponse(WarehouseBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class InventoryBase(BaseModel):
    warehouse_id: UUID
    product_id: UUID
    quantity_on_hand: float = 0
    reorder_level: Optional[float] = 10

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity_on_hand: Optional[float] = None
    reorder_level: Optional[float] = None
    is_active: Optional[bool] = None

class InventoryResponse(InventoryBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
