import pytest, uuid
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_register_and_login():
    transport = ASGITransport(app=app, root_path="")
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:

        # ✅ Generate unique username
        unique_username = f"testuser_{uuid.uuid4().hex[:6]}"

        # 1️⃣ Register
        register_response = await ac.post("/auth/register", json={
            "username": unique_username,
            "password": "testpass",
            "email": f"{unique_username}@example.com"
        })
        print("Register status:", register_response.status_code, register_response.json())
        assert register_response.status_code == 201

        # 2️⃣ Login
        login_response = await ac.post("/auth/login", json={
            "username": unique_username,
            "password": "testpass"
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # 3️⃣ Access /me
        me_response = await ac.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert me_response.status_code == 200
        assert me_response.json()["username"] == unique_username

