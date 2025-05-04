import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_families_crud():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # 1) изначально пусто
        r = await ac.get("/families")
        assert r.status_code == 200 and r.json() == []

        # 2) создаём семью
        payload = {"group_name": "TestFam", "tags": ["food", "books"]}
        r = await ac.post("/families", json=payload)
        assert r.status_code == 201
        fid = r.json()["id"]             # <-- changed

        # 3) список содержит новую
        r = await ac.get("/families")
        assert any(f["id"] == fid and f["group_name"] == "TestFam" for f in r.json())

        # 4) получаем по id
        r = await ac.get(f"/families/{fid}")
        assert r.status_code == 200 and r.json()["group_name"] == "TestFam"

        # 5) обновляем
        upd = {"group_name": "NewName", "tags": ["x"]}
        r = await ac.put(f"/families/{fid}", json=upd)
        assert r.status_code == 200 and r.json() == {"status": "success"}
        r = await ac.get(f"/families/{fid}")
        assert r.json()["group_name"] == "NewName" and r.json()["tags"] == ["x"]

        # 6) удаляем
        r = await ac.delete(f"/families/{fid}")
        assert r.status_code == 200 and r.json() == {"status": "success"}
        r = await ac.get(f"/families/{fid}")
        assert r.status_code == 404