from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.database.session import get_db
from app.schemas.response import StandardResponse
from app.schemas.catalog import CategoryCreate, CategoryUpdate, CategoryResponse, ProductCreate, ProductUpdate, ProductResponse
from app.services.catalog import category_service, product_service
from app.api.dependencies import get_current_manager, get_current_user

router = APIRouter(prefix="/catalog", tags=["Catalog"])

# ================= Categories =================

@router.get("/categories", response_model=StandardResponse[List[CategoryResponse]])
async def get_categories(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=1000), 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user)
):
    categories = await category_service.get_multi(db, skip=skip, limit=limit)
    return StandardResponse(success=True, message="Categories retrieved", data=categories["data"], total_records=categories["total_records"], total_pages=categories["total_pages"], page=categories["page"], limit=categories["limit"])

@router.get("/categories/{id}", response_model=StandardResponse[CategoryResponse])
async def get_category(id: UUID, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    category = await category_service.get(db, id=id)
    return StandardResponse(success=True, message="Category retrieved", data=category["data"], total_records=category["total_records"], total_pages=category["total_pages"], page=category["page"], limit=category["limit"])

@router.post("/categories", response_model=StandardResponse[CategoryResponse])
async def create_category(
    category_in: CategoryCreate, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    category = await category_service.create(db, obj_in=category_in)
    return StandardResponse(success=True, message="Category created", data=category["data"], total_records=category["total_records"], total_pages=category["total_pages"], page=category["page"], limit=category["limit"])

@router.put("/categories/{id}", response_model=StandardResponse[CategoryResponse])
async def update_category(
    id: UUID, 
    category_in: CategoryUpdate, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    category = await category_service.update(db, id=id, obj_in=category_in)
    return StandardResponse(success=True, message="Category updated", data=category["data"], total_records=category["total_records"], total_pages=category["total_pages"], page=category["page"], limit=category["limit"])

@router.delete("/categories/{id}", response_model=StandardResponse[CategoryResponse])
async def delete_category(
    id: UUID, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    category = await category_service.remove(db, id=id)
    return StandardResponse(success=True, message="Category deleted", data=category["data"], total_records=category["total_records"], total_pages=category["total_pages"], page=category["page"], limit=category["limit"])

# ================= Products =================

@router.get("/products", response_model=StandardResponse[List[ProductResponse]])
async def get_products(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=1000), 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user)
):
    products = await product_service.get_multi(db, skip=skip, limit=limit)
    return StandardResponse(success=True, message="Products retrieved", data=products["data"], total_records=products["total_records"], total_pages=products["total_pages"], page=products["page"], limit=products["limit"])

@router.get("/products/{id}", response_model=StandardResponse[ProductResponse])
async def get_product(id: UUID, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    product = await product_service.get(db, id=id)
    return StandardResponse(success=True, message="Product retrieved", data=product["data"], total_records=product["total_records"], total_pages=product["total_pages"], page=product["page"], limit=product["limit"])

@router.post("/products", response_model=StandardResponse[ProductResponse])
async def create_product(
    product_in: ProductCreate, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    product = await product_service.create(db, obj_in=product_in)
    return StandardResponse(success=True, message="Product created", data=product["data"], total_records=product["total_records"], total_pages=product["total_pages"], page=product["page"], limit=product["limit"])

@router.put("/products/{id}", response_model=StandardResponse[ProductResponse])
async def update_product(
    id: UUID, 
    product_in: ProductUpdate, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    product = await product_service.update(db, id=id, obj_in=product_in)
    return StandardResponse(success=True, message="Product updated", data=product["data"], total_records=product["total_records"], total_pages=product["total_pages"], page=product["page"], limit=product["limit"])

@router.delete("/products/{id}", response_model=StandardResponse[ProductResponse])
async def delete_product(
    id: UUID, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    product = await product_service.remove(db, id=id)
    return StandardResponse(success=True, message="Product deleted", data=product["data"], total_records=product["total_records"], total_pages=product["total_pages"], page=product["page"], limit=product["limit"])
