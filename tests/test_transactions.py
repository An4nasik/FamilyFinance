import re
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_transactions_crud():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Подготовка: создаем семью и пользователя
        fam = await ac.post("/families", json={"group_name": "TX", "tags": []})
        fid = fam.json()["id"]
        user = await ac.post(f"/families/{fid}/users", json={
            "name": "Bob", "email": "bob@example.com", "password": "pwd"
        })
        uid = user.json()["id"]

        # Создаем покупку с новым тегом
        buy = await ac.post(f"/families/{fid}/purchases", json={
            "user_id": uid, "price": 50.5, "tags": ["новый_тег"], "date": "01.01.2025"
        })
        assert buy.status_code == 201

        # Проверяем, что новый тег добавился в семью
        fam = await ac.get(f"/families/{fid}")
        assert "новый_тег" in fam.json()["tags"]  # Проверяем, что тег добавился