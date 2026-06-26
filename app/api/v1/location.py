from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.database.session import get_db
from app.schemas.response import StandardResponse
from app.schemas.location import (
    CountryCreate, CountryUpdate, CountryResponse,
    StoreCreate, StoreBase, StoreResponse,
    DepartmentCreate, DepartmentBase, DepartmentResponse
)
from app.services.location import country_service, store_service, department_service
from app.api.dependencies import get_current_manager, get_current_user

router = APIRouter(prefix="/location", tags=["Location"])

# ================= Countries =================

@router.get("/countries", response_model=StandardResponse[List[CountryResponse]])
async def get_countries(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=1000), 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user)
):
    countries = await country_service.get_multi(db, skip=skip, limit=limit)
    return StandardResponse(success=True, message="Countries retrieved", data=countries["data"], total_records=countries["total_records"], total_pages=countries["total_pages"], page=countries["page"], limit=countries["limit"])

@router.get("/countries/{id}", response_model=StandardResponse[CountryResponse])
async def get_country(id: UUID, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    country = await country_service.get(db, id=id)
    return StandardResponse(success=True, message="Country retrieved", data=country["data"], total_records=country["total_records"], total_pages=country["total_pages"], page=country["page"], limit=country["limit"])

@router.post("/countries", response_model=StandardResponse[CountryResponse])
async def create_country(
    country_in: CountryCreate, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    country = await country_service.create(db, obj_in=country_in)
    return StandardResponse(success=True, message="Country created", data=country["data"], total_records=country["total_records"], total_pages=country["total_pages"], page=country["page"], limit=country["limit"])

# ================= Stores =================

@router.get("/stores", response_model=StandardResponse[List[StoreResponse]])
async def get_stores(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=1000), 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user)
):
    stores = await store_service.get_multi(db, skip=skip, limit=limit)
    return StandardResponse(success=True, message="Stores retrieved", data=stores["data"], total_records=stores["total_records"], total_pages=stores["total_pages"], page=stores["page"], limit=stores["limit"])

@router.get("/stores/{id}", response_model=StandardResponse[StoreResponse])
async def get_store(id: UUID, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    store = await store_service.get(db, id=id)
    return StandardResponse(success=True, message="Store retrieved", data=store["data"], total_records=store["total_records"], total_pages=store["total_pages"], page=store["page"], limit=store["limit"])

@router.post("/stores", response_model=StandardResponse[StoreResponse])
async def create_store(
    store_in: StoreCreate, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    store = await store_service.create(db, obj_in=store_in)
    return StandardResponse(success=True, message="Store created", data=store["data"], total_records=store["total_records"], total_pages=store["total_pages"], page=store["page"], limit=store["limit"])

# ================= Departments =================

@router.get("/departments", response_model=StandardResponse[List[DepartmentResponse]])
async def get_departments(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=1000), 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user)
):
    departments = await department_service.get_multi(db, skip=skip, limit=limit)
    return StandardResponse(success=True, message="Departments retrieved", data=departments["data"], total_records=departments["total_records"], total_pages=departments["total_pages"], page=departments["page"], limit=departments["limit"])

@router.get("/departments/{id}", response_model=StandardResponse[DepartmentResponse])
async def get_department(id: UUID, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    department = await department_service.get(db, id=id)
    return StandardResponse(success=True, message="Department retrieved", data=department["data"], total_records=department["total_records"], total_pages=department["total_pages"], page=department["page"], limit=department["limit"])

@router.post("/departments", response_model=StandardResponse[DepartmentResponse])
async def create_department(
    department_in: DepartmentCreate, 
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_manager)
):
    department = await department_service.create(db, obj_in=department_in)
    return StandardResponse(success=True, message="Department created", data=department["data"], total_records=department["total_records"], total_pages=department["total_pages"], page=department["page"], limit=department["limit"])
