from app.services.base import BaseService
from app.models.people import Customer, Supplier, Employee
from app.schemas.people import (
    CustomerCreate, CustomerUpdate, 
    SupplierCreate, SupplierUpdate, 
    EmployeeCreate, EmployeeUpdate
)
from app.repositories.people import customer_repo, supplier_repo, employee_repo

class CustomerService(BaseService[Customer, CustomerCreate, CustomerUpdate]):
    pass

class SupplierService(BaseService[Supplier, SupplierCreate, SupplierUpdate]):
    pass

class EmployeeService(BaseService[Employee, EmployeeCreate, EmployeeUpdate]):
    pass

customer_service = CustomerService(customer_repo)
supplier_service = SupplierService(supplier_repo)
employee_service = EmployeeService(employee_repo)
