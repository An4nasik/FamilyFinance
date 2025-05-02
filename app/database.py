import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
from app.config import settings

logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self):
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DB]

    async def init_db(self):
        # создаём уникальные и вспомогательные индексы
        return self

    def coll(self, name: str):
        return self.db[name]


mongodb = MongoDB()