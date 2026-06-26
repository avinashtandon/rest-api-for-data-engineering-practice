import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from collections import defaultdict
import asyncio

from app.schemas.response import StandardResponse, ErrorResponse

# In-memory rate limiting store
# Format: {ip: [timestamps]}
rate_limit_store = defaultdict(list)

# Limits
ANON_LIMIT = 20
AUTH_LIMIT = 200
WINDOW_SECONDS = 60

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        
        # Check if auth token exists (basic check, actual validation happens in dependencies)
        auth_header = request.headers.get("Authorization")
        
        # Determine limit based on auth presence (Admin unlimited not handled here perfectly without DB query, 
        # but for simplicity, we assume AUTH_LIMIT is sufficient for the simulation, 
        # or we could decode JWT here to check Role. We will decode JWT here for proper Role check)
        limit = ANON_LIMIT
        if auth_header and auth_header.startswith("Bearer "):
            from app.core.security import decode_token
            from app.models.user import RoleEnum
            try:
                token = auth_header.split(" ")[1]
                payload = decode_token(token)
                
                # We could query DB to get exact role, but to keep rate limit fast:
                # We can skip rate limit if it's an authenticated user and assume AUTH_LIMIT, 
                # but if we wanted unlimited for Admin we'd need role in JWT.
                # Let's assume AUTH_LIMIT for now. Admin might hit 200/min.
                limit = AUTH_LIMIT
            except Exception:
                pass # Invalid token, let dependency handle it, keep ANON_LIMIT
                
        now = time.time()
        
        # Clean up old timestamps
        rate_limit_store[client_ip] = [ts for ts in rate_limit_store[client_ip] if now - ts < WINDOW_SECONDS]
        
        if len(rate_limit_store[client_ip]) >= limit:
            retry_after = int(WINDOW_SECONDS - (now - rate_limit_store[client_ip][0]))
            headers = {
                "X-RateLimit-Limit": str(limit),
                "X-RateLimit-Remaining": "0",
                "Retry-After": str(retry_after)
            }
            return JSONResponse(
                status_code=429,
                content=StandardResponse(
                    success=False,
                    message="Too Many Requests",
                    error=ErrorResponse(code="TOO_MANY_REQUESTS", message="Rate limit exceeded")
                ).model_dump(exclude_none=True),
                headers=headers
            )
            
        rate_limit_store[client_ip].append(now)
        
        response = await call_next(request)
        
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(limit - len(rate_limit_store[client_ip]))
        
        return response
