from app.services.base import BaseService
from app.models.catalog import Category, Product
from app.schemas.catalog import CategoryCreate, CategoryUpdate, ProductCreate, ProductUpdate
from app.repositories.catalog import category_repo, product_repo

class CategoryService(BaseService[Category, CategoryCreate, CategoryUpdate]):
    pass

class ProductService(BaseService[Product, ProductCreate, ProductUpdate]):
    pass

category_service = CategoryService(category_repo)
product_service = ProductService(product_repo)
