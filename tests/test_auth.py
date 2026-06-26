import pytest
import uuid

@pytest.mark.anyio
async def test_register_and_login(async_client):
    # Test Register
    unique_email = f"test_{uuid.uuid4()}@example.com"
    response = await async_client.post("/api/v1/auth/register", json={
        "email": unique_email,
        "first_name": "Test",
        "last_name": "User",
        "password": "Password123!",
        "role": "Viewer"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == unique_email
    
    # Test Login
    login_resp = await async_client.post("/api/v1/auth/login", json={
        "email": unique_email,
        "password": "Password123!"
    })
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    assert login_data["success"] is True
    assert "access_token" in login_data["data"]
