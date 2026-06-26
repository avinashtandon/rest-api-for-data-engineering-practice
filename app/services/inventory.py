from app.services.base import BaseService
from app.models.inventory import Warehouse, Inventory
from app.schemas.inventory import WarehouseCreate, WarehouseUpdate, InventoryCreate, InventoryUpdate
from app.repositories.inventory import warehouse_repo, inventory_repo

class WarehouseService(BaseService[Warehouse, WarehouseCreate, WarehouseUpdate]):
    pass

class InventoryService(BaseService[Inventory, InventoryCreate, InventoryUpdate]):
    pass

warehouse_service = WarehouseService(warehouse_repo)
inventory_service = InventoryService(inventory_repo)
