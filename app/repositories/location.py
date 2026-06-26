from app.repositories.base import BaseRepository
from app.models.location import Country, State, City, Address, Store, Department
from app.schemas.location import (
    CountryCreate, CountryUpdate,
    StateCreate, StateBase,
    CityCreate, CityBase,
    AddressCreate, AddressBase,
    StoreCreate, StoreBase,
    DepartmentCreate, DepartmentBase
)

class CountryRepository(BaseRepository[Country, CountryCreate, CountryUpdate]):
    pass

class StateRepository(BaseRepository[State, StateCreate, StateBase]):
    pass

class CityRepository(BaseRepository[City, CityCreate, CityBase]):
    pass

class AddressRepository(BaseRepository[Address, AddressCreate, AddressBase]):
    pass

class StoreRepository(BaseRepository[Store, StoreCreate, StoreBase]):
    pass

class DepartmentRepository(BaseRepository[Department, DepartmentCreate, DepartmentBase]):
    pass

country_repo = CountryRepository(Country)
state_repo = StateRepository(State)
city_repo = CityRepository(City)
address_repo = AddressRepository(Address)
store_repo = StoreRepository(Store)
department_repo = DepartmentRepository(Department)
