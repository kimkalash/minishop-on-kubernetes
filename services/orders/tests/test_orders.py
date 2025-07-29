import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_create_and_get_order():
    transport = ASGITransport(app=app, root_path="")
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/orders/orders", json={"user_id": 1, "total_price": 50.0})
        assert response.status_code == 201
        order_id = response.json()["id"]

        get_response = await ac.get(f"/orders/orders/{order_id}")
        assert get_response.status_code == 200
        assert get_response.json()["total_price"] == 50.0
