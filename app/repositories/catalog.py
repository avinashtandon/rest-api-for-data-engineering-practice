from app.repositories.base import BaseRepository
from app.models.catalog import Category, Product
from app.schemas.catalog import CategoryCreate, CategoryUpdate, ProductCreate, ProductUpdate

class CategoryRepository(BaseRepository[Category, CategoryCreate, CategoryUpdate]):
    pass

class ProductRepository(BaseRepository[Product, ProductCreate, ProductUpdate]):
    pass

category_repo = CategoryRepository(Category)
product_repo = ProductRepository(Product)
