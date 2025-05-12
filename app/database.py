import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self):
        # Это проявление удивительных костыльных технологий имени меня.
        # Я не смог поднять отдельно ДБ на тесты, поэтому меняем тут ссылки чтобы протестить.....
        # self.client: AsyncIOMotorClient = AsyncIOMotorClient(settings.TEST_MONGO_URI)
        # self.db = self.client[settings.TEST_MONGO_DB]
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DB]

    async def init_db(self):
        # создаём уникальные и вспомогательные индексы
        return self

    def coll(self, name: str):
        return self.db[name]

# Вот эта хуйня кстати не работает, но если ее убрать, тесты не будут работать...
class TestMongoDB:
    def __init__(self):
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(settings.TEST_MONGO_URI)
        self.db = self.client[settings.TEST_MONGO_DB]

    async def init_db(self):
        # создаём уникальные и вспомогательные индексы
        return self

    def coll(self, name: str):
        return self.db[name]


test_mongodb = TestMongoDB()



mongodb = MongoDB()