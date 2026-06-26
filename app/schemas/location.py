from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class CountryBase(BaseModel):
    name: str
    code: str

class CountryCreate(CountryBase):
    pass

class CountryUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None

class CountryResponse(CountryBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class StateBase(BaseModel):
    name: str
    code: Optional[str] = None
    country_id: UUID

class StateCreate(StateBase):
    pass

class StateResponse(StateBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CityBase(BaseModel):
    name: str
    state_id: UUID

class CityCreate(CityBase):
    pass

class CityResponse(CityBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AddressBase(BaseModel):
    line1: str
    line2: Optional[str] = None
    postal_code: str
    city_id: UUID

class AddressCreate(AddressBase):
    pass

class AddressResponse(AddressBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class StoreBase(BaseModel):
    name: str
    address_id: Optional[UUID] = None
    phone: Optional[str] = None

class StoreCreate(StoreBase):
    pass

class StoreResponse(StoreBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DepartmentBase(BaseModel):
    name: str
    store_id: Optional[UUID] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
