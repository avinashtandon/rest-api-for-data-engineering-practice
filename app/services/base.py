from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from pydantic import BaseModel

from app.models.base import Base
from app.repositories.base import BaseRepository
from app.exceptions.custom import NotFoundException

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, repository: BaseRepository[ModelType, CreateSchemaType, UpdateSchemaType]):
        self.repository = repository

    async def get(self, db: AsyncSession, id: UUID) -> ModelType:
        obj = await self.repository.get(db, id)
        if not obj:
            raise NotFoundException(message=f"{self.repository.model.__name__} not found")
        return obj

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
        return await self.repository.get_multi(
            db, 
            skip=skip, 
            limit=limit, 
            filters=filters,
            sort_by=sort_by,
            order=order,
            fields=fields,
            cursor=cursor
        )

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        return await self.repository.create(db, obj_in=obj_in)

    async def update(self, db: AsyncSession, *, id: UUID, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        db_obj = await self.get(db, id)
        return await self.repository.update(db, db_obj=db_obj, obj_in=obj_in)

    async def remove(self, db: AsyncSession, *, id: UUID) -> ModelType:
        db_obj = await self.get(db, id)
        return await self.repository.remove(db, id=id)
