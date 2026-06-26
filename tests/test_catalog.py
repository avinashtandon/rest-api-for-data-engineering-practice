import pytest
import uuid

@pytest.fixture
async def auth_headers(async_client):
    unique_email = f"test_{uuid.uuid4()}@example.com"
    await async_client.post("/api/v1/auth/register", json={
        "email": unique_email,
        "first_name": "Test",
        "last_name": "User",
        "password": "Password123!",
        "role": "Viewer"
    })
    resp = await async_client.post("/api/v1/auth/login", json={
        "email": unique_email,
        "password": "Password123!"
    })
    token = resp.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.anyio
async def test_get_categories(async_client, auth_headers):
    response = await async_client.get("/api/v1/catalog/categories", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

@pytest.mark.anyio
async def test_get_products(async_client, auth_headers):
    response = await async_client.get("/api/v1/catalog/products", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
