from app.repositories.base import BaseRepository
from app.models.people import Customer, Supplier, Employee
from app.schemas.people import (
    CustomerCreate, CustomerUpdate, 
    SupplierCreate, SupplierUpdate, 
    EmployeeCreate, EmployeeUpdate
)

class CustomerRepository(BaseRepository[Customer, CustomerCreate, CustomerUpdate]):
    pass

class SupplierRepository(BaseRepository[Supplier, SupplierCreate, SupplierUpdate]):
    pass

class EmployeeRepository(BaseRepository[Employee, EmployeeCreate, EmployeeUpdate]):
    pass

customer_repo = CustomerRepository(Customer)
supplier_repo = SupplierRepository(Supplier)
employee_repo = EmployeeRepository(Employee)
