import pytest
from app.database import test_mongodb

@pytest.fixture(scope="module", autouse=True)
async def init_db():
    # инициализируем БД (индексы и т.п.) перед тестами модуля
    await test_mongodb.init_db()
    yield

@pytest.fixture(autouse=True)
async def clear_db():
    # чистим коллекции перед каждым тестом
    await test_mongodb.db.drop_collection("families")
    await test_mongodb.db.drop_collection("users")
    await test_mongodb.db.drop_collection("transactions")
    yield