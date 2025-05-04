import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_users_crud():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Создаем семью
        fam = await ac.post("/families", json={"group_name": "FamU", "tags": []})
        fid = fam.json()["id"]

        # Добавляем пользователя
        user_data = {"name": "Alice", "email": "alice@example.com", "password": "secret"}
        r = await ac.post(f"/families/{fid}/users", json=user_data)
        assert r.status_code == 201
        uid = r.json()["id"]

        # Проверяем, что пользователь добавлен в семью
        fam = await ac.get(f"/families/{fid}")
        assert uid in fam.json()["users"]

        # Проверяем, что нельзя добавить пользователя с той же почтой
        r = await ac.post(f"/families/{fid}/users", json=user_data)
        assert r.status_code == 400  # Ожидаем ошибку 400
        assert "User with this email already exists" in r.json()["detail"]  # Проверяем, что сообщение содержит ожидаемый текст