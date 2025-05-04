import pytest
from app.database import mongodb

@pytest.fixture(scope="module", autouse=True)
async def init_db():
    # инициализируем БД (индексы и т.п.) перед тестами модуля
    await mongodb.init_db()
    yield

@pytest.fixture(autouse=True)
async def clear_db():
    # чистим коллекции перед каждым тестом
    await mongodb.db.drop_collection("families")
    await mongodb.db.drop_collection("users")
    await mongodb.db.drop_collection("transactions")
    yield