from typing import Generic, TypeVar, Optional, List, Any
from pydantic import BaseModel, Field

T = TypeVar("T")

class ErrorResponse(BaseModel):
    code: str
    message: str
    trace_id: Optional[str] = None

class StandardResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    page: Optional[int] = None
    limit: Optional[int] = None
    total_records: Optional[int] = None
    total_pages: Optional[int] = None
    next_page: Optional[int] = None
    previous_page: Optional[int] = None
    execution_time_ms: Optional[int] = None
    data: Optional[T] = None
    error: Optional[ErrorResponse] = None
