from app.services.base import BaseService
from app.models.location import Country, State, City, Address, Store, Department
from app.schemas.location import (
    CountryCreate, CountryUpdate,
    StateCreate, StateBase,
    CityCreate, CityBase,
    AddressCreate, AddressBase,
    StoreCreate, StoreBase,
    DepartmentCreate, DepartmentBase
)
from app.repositories.location import (
    country_repo, state_repo, city_repo, 
    address_repo, store_repo, department_repo
)

class CountryService(BaseService[Country, CountryCreate, CountryUpdate]):
    pass

class StateService(BaseService[State, StateCreate, StateBase]):
    pass

class CityService(BaseService[City, CityCreate, CityBase]):
    pass

class AddressService(BaseService[Address, AddressCreate, AddressBase]):
    pass

class StoreService(BaseService[Store, StoreCreate, StoreBase]):
    pass

class DepartmentService(BaseService[Department, DepartmentCreate, DepartmentBase]):
    pass

country_service = CountryService(country_repo)
state_service = StateService(state_repo)
city_service = CityService(city_repo)
address_service = AddressService(address_repo)
store_service = StoreService(store_repo)
department_service = DepartmentService(department_repo)
