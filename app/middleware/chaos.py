import random
import asyncio
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.schemas.response import StandardResponse, ErrorResponse

class ChaosMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not settings.SIMULATE_CHAOS:
            return await call_next(request)
            
        # Simulate Latency
        if random.random() < settings.CHAOS_LATENCY_RATE:
            delay_ms = random.uniform(100, settings.CHAOS_MAX_LATENCY_MS)
            await asyncio.sleep(delay_ms / 1000.0)
            
        # Simulate Errors
        if random.random() < settings.CHAOS_ERROR_RATE:
            error_types = [
                (500, "INTERNAL_SERVER_ERROR", "Simulated Internal Server Error"),
                (503, "SERVICE_UNAVAILABLE", "Simulated Service Unavailable"),
                (429, "TOO_MANY_REQUESTS", "Simulated Rate Limit Exceeded")
            ]
            status_code, code, message = random.choice(error_types)
            return JSONResponse(
                status_code=status_code,
                content=StandardResponse(
                    success=False,
                    message=message,
                    error=ErrorResponse(code=code, message=message)
                ).model_dump(exclude_none=True)
            )
            
        return await call_next(request)
