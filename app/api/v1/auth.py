from fastapi import APIRouter, Depends, BackgroundTasks, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from app.database.session import get_db
from app.models.user import User
from app.schemas.auth import (
    LoginRequest, TokenResponse, RefreshRequest, 
    ChangePasswordRequest, ForgotPasswordRequest, ResetPasswordRequest
)
from app.schemas.user import UserCreate, UserResponse
from app.schemas.response import StandardResponse
from app.core.security import (
    verify_password, get_password_hash, 
    create_access_token, create_refresh_token, decode_token
)
from app.api.dependencies import get_current_user
from app.exceptions.custom import BadRequestException, UnauthorizedException, NotFoundException
from app.core.logger import logger

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=StandardResponse[UserResponse])
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    stmt = select(User).where(User.email == user_in.email)
    result = await db.execute(stmt)
    if result.scalars().first():
        raise BadRequestException(message="User with this email already exists")

    new_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        phone_number=user_in.phone_number,
        role=user_in.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return StandardResponse(
        success=True,
        message="User registered successfully",
        data=new_user
    )

@router.post("/login", response_model=StandardResponse[TokenResponse])
async def login(request: Request, login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == login_data.email)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise UnauthorizedException(message="Invalid email or password")
    
    if not user.is_active or user.is_locked or user.deleted_at:
        raise UnauthorizedException(message="Account is inactive, locked, or deleted")

    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)

    # Save refresh token for revocation and rotation
    user.refresh_token = get_password_hash(refresh_token)
    user.updated_at = datetime.utcnow()
    await db.commit()

    from app.core.config import settings
    return StandardResponse(
        success=True,
        message="Login successful",
        data=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    )

@router.post("/refresh", response_model=StandardResponse[TokenResponse])
async def refresh_token(request_data: RefreshRequest, db: AsyncSession = Depends(get_db)):
    payload = decode_token(request_data.refresh_token)
    if payload.get("type") != "refresh":
        raise UnauthorizedException(message="Invalid token type")

    user_id = payload.get("sub")
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user or not user.is_active or user.is_locked or user.deleted_at:
        raise UnauthorizedException(message="Invalid user state")
        
    if not user.refresh_token or not verify_password(request_data.refresh_token, user.refresh_token):
        raise UnauthorizedException(message="Refresh token is revoked or invalid")

    access_token = create_access_token(subject=user.id)
    new_refresh_token = create_refresh_token(subject=user.id)

    user.refresh_token = get_password_hash(new_refresh_token)
    user.updated_at = datetime.utcnow()
    await db.commit()

    from app.core.config import settings
    return StandardResponse(
        success=True,
        message="Token refreshed successfully",
        data=TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    )

@router.post("/logout", response_model=StandardResponse[dict])
async def logout(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    current_user.refresh_token = None
    await db.commit()
    return StandardResponse(
        success=True,
        message="Logged out successfully",
        data={}
    )

@router.post("/change-password", response_model=StandardResponse[dict])
async def change_password(
    password_data: ChangePasswordRequest, 
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise BadRequestException(message="Invalid old password")
        
    current_user.hashed_password = get_password_hash(password_data.new_password)
    # Revoke tokens
    current_user.refresh_token = None
    await db.commit()
    
    return StandardResponse(
        success=True,
        message="Password changed successfully. Please login again.",
        data={}
    )
