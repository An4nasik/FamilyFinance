import pytest
from httpx import AsyncClient
from app.main import app
from app.database import mongodb

@pytest.fixture(autouse=True, scope="module")
async def init_db():
    await mongodb.init_db()
    yield

@pytest.mark.anyio
async def test_create_and_get_family():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/families", json={"group_name":"TestFam","tags":["food"]})
        assert resp.status_code == 201
        fid = resp.json()["family_id"]

        resp = await ac.get("/families")
        assert resp.status_code == 200
        data = resp.json()
        assert any(f["id"] == fid for f in data)

        resp = await ac.get(f"/families/{fid}")
        assert resp.status_code == 200
        assert resp.json()["group_name"] == "TestFam"