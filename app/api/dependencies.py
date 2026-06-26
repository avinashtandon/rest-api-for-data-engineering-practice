from fastapi import Depends, Request, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import exc
from uuid import UUID
from typing import Optional
from datetime import datetime

from app.database.session import get_db
from app.core.security import decode_token
from app.models.user import User, RoleEnum
from app.exceptions.custom import UnauthorizedException, ForbiddenException
from app.core.logger import logger

security = HTTPBearer()

async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    token = credentials.credentials
    try:
        payload = decode_token(token)
    except Exception as e:
        logger.warning(f"Failed to decode token: {str(e)}", extra={"trace_id": getattr(request.state, "request_id", None)})
        raise
    
    if payload.get("type") != "access":
        raise UnauthorizedException(message="Invalid token type")
        
    user_id = payload.get("sub")
    if user_id is None:
        raise UnauthorizedException(message="Invalid token payload")

    try:
        uuid_user_id = UUID(user_id)
    except ValueError:
        raise UnauthorizedException(message="Invalid user ID format")

    stmt = select(User).where(User.id == uuid_user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise UnauthorizedException(message="User not found")
        
    if not user.is_active:
        raise UnauthorizedException(message="Inactive user")
        
    if user.is_locked:
        raise UnauthorizedException(message="Locked user")
        
    # Check if deleted
    if user.deleted_at is not None:
        raise UnauthorizedException(message="Deleted user")

    return user


class RoleChecker:
    def __init__(self, allowed_roles: list[RoleEnum]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise ForbiddenException(message="You do not have enough permissions to perform this action")
        return user

# Pre-defined dependencies for RBAC
get_current_admin = RoleChecker([RoleEnum.ADMIN])
get_current_manager = RoleChecker([RoleEnum.ADMIN, RoleEnum.MANAGER])
get_current_data_engineer = RoleChecker([RoleEnum.ADMIN, RoleEnum.DATA_ENGINEER])
get_current_analyst = RoleChecker([RoleEnum.ADMIN, RoleEnum.ANALYST, RoleEnum.MANAGER])
# Viewer can be everyone logged in

async def get_query_params(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sort_by: Optional[str] = Query(None),
    order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
    fields: Optional[str] = Query(None),
    cursor: Optional[str] = Query(None),
    updated_after: Optional[datetime] = Query(None),
    created_after: Optional[datetime] = Query(None),
    q: Optional[str] = Query(None, description="Full text search query")
) -> dict:
    return {
        "skip": skip,
        "limit": limit,
        "sort_by": sort_by,
        "order": order,
        "fields": fields,
        "cursor": cursor,
        "filters": {
            "updated_after": updated_after,
            "created_after": created_after,
            "q": q
        }
    }
