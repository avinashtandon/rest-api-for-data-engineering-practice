from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete, func, select
from pydantic import BaseModel
from uuid import UUID

from app.models.base import Base
from app.utils.query_builder import QueryBuilder

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id, self.model.deleted_at == None)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_multi(
        self, 
        db: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        filters: Dict[str, Any] = None,
        sort_by: str = None,
        order: str = "asc",
        fields: str = None,
        cursor: str = None
    ) -> dict:
        builder = QueryBuilder(self.model)
        stmt = select(self.model).where(self.model.deleted_at == None)
        
        if filters:
            stmt = builder.apply_filters(stmt, filters)
            
        # Get total count before pagination
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_records = await db.scalar(count_stmt)
            
        stmt = builder.apply_sorting(stmt, sort_by, order)
        stmt = builder.apply_field_selection(stmt, fields)
        
        if cursor:
            stmt = builder.apply_cursor_pagination(stmt, cursor, limit)
        else:
            stmt = builder.apply_pagination(stmt, skip, limit)
            
        result = await db.execute(stmt)
        data = list(result.scalars().all())
        
        total_pages = (total_records + limit - 1) // limit if total_records else 0
        current_page = (skip // limit) + 1 if limit else 1
        
        return {
            "data": data,
            "total_records": total_records,
            "total_pages": total_pages,
            "page": current_page,
            "limit": limit,
            "next_page": current_page + 1 if current_page < total_pages else None,
            "previous_page": current_page - 1 if current_page > 1 else None
        }

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        obj_data = db_obj.__dict__
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
            
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
                
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: UUID) -> ModelType:
        # We perform a soft delete
        from datetime import datetime
        stmt = select(self.model).where(self.model.id == id)
        result = await db.execute(stmt)
        obj = result.scalars().first()
        if obj:
            obj.deleted_at = datetime.utcnow()
            obj.is_active = False
            db.add(obj)
            await db.commit()
        return obj
