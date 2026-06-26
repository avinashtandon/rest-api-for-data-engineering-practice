from app.repositories.base import BaseRepository
from app.models.inventory import Warehouse, Inventory
from app.schemas.inventory import WarehouseCreate, WarehouseUpdate, InventoryCreate, InventoryUpdate

class WarehouseRepository(BaseRepository[Warehouse, WarehouseCreate, WarehouseUpdate]):
    pass

class InventoryRepository(BaseRepository[Inventory, InventoryCreate, InventoryUpdate]):
    pass

warehouse_repo = WarehouseRepository(Warehouse)
inventory_repo = InventoryRepository(Inventory)
