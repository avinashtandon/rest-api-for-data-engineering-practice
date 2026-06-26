from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.exceptions.handlers import register_exception_handlers
from app.middleware.request import RequestMiddleware
from app.middleware.chaos import ChaosMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.schemas.response import StandardResponse
from app.api.v1.auth import router as auth_router
from app.api.v1.catalog import router as catalog_router
from app.api.v1.people import router as people_router
from app.api.v1.location import router as location_router
from app.api.v1.transactions import router as transactions_router
from app.api.v1.inventory import router as inventory_router
from app.api.v1.export import router as export_router

def get_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Custom Middlewares
    app.add_middleware(RequestMiddleware)
    app.add_middleware(ChaosMiddleware)
    app.add_middleware(RateLimitMiddleware)

    # Exception Handlers
    register_exception_handlers(app)

    # Health Check
    @app.get("/health", response_model=StandardResponse[dict], tags=["System"])
    async def health_check():
        return StandardResponse(
            success=True,
            message="System is healthy",
            data={"status": "ok"}
        )

    # API Routers
    app.include_router(auth_router, prefix=settings.API_V1_STR)
    app.include_router(catalog_router, prefix=settings.API_V1_STR)
    app.include_router(people_router, prefix=settings.API_V1_STR)
    app.include_router(location_router, prefix=settings.API_V1_STR)
    app.include_router(transactions_router, prefix=settings.API_V1_STR)
    app.include_router(inventory_router, prefix=settings.API_V1_STR)
    app.include_router(export_router, prefix=settings.API_V1_STR)

    return app

app = get_application()
