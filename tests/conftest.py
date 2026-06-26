import pytest
from httpx import AsyncClient, ASGITransport
import asyncio

from main import get_application
from app.database.session import engine, get_db

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
def app():
    return get_application()

@pytest.fixture(scope="function")
async def async_client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        yield client
