from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import traceback

from app.schemas.response import StandardResponse, ErrorResponse
from app.exceptions.custom import APIException
from app.core.logger import logger

async def custom_api_exception_handler(request: Request, exc: APIException):
    trace_id = getattr(request.state, "request_id", None)
    logger.warning(f"APIException: {exc.message}", extra={"trace_id": trace_id})
    return JSONResponse(
        status_code=exc.status_code,
        content=StandardResponse(
            success=False,
            message=exc.message,
            error=ErrorResponse(code=exc.code, message=exc.message, trace_id=trace_id)
        ).model_dump(exclude_none=True)
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    trace_id = getattr(request.state, "request_id", None)
    logger.warning(f"Validation error: {exc.errors()}", extra={"trace_id": trace_id})
    return JSONResponse(
        status_code=422,
        content=StandardResponse(
            success=False,
            message="Validation error",
            error=ErrorResponse(code="VALIDATION_ERROR", message=str(exc.errors()), trace_id=trace_id)
        ).model_dump(exclude_none=True)
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    trace_id = getattr(request.state, "request_id", None)
    logger.error(f"Database error: {str(exc)}", exc_info=True, extra={"trace_id": trace_id})
    return JSONResponse(
        status_code=500,
        content=StandardResponse(
            success=False,
            message="Database error occurred",
            error=ErrorResponse(code="DATABASE_ERROR", message="An internal database error occurred", trace_id=trace_id)
        ).model_dump(exclude_none=True)
    )

async def general_exception_handler(request: Request, exc: Exception):
    trace_id = getattr(request.state, "request_id", None)
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True, extra={"trace_id": trace_id})
    return JSONResponse(
        status_code=500,
        content=StandardResponse(
            success=False,
            message="Internal server error",
            error=ErrorResponse(code="INTERNAL_SERVER_ERROR", message="An unexpected error occurred", trace_id=trace_id)
        ).model_dump(exclude_none=True)
    )

def register_exception_handlers(app):
    app.add_exception_handler(APIException, custom_api_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
