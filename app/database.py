from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.family_models import Family, User, Purchase
import os  # Импортируем модуль для работы с переменными окружения


async def init_db():
    # Берем URL из переменной окружения, если ее нет — используем значение по умолчанию
    mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/family_finance_db")

    client = AsyncIOMotorClient(mongo_url)
    await init_beanie(
        database=client.family_finance_db,  # Явно указываем имя БД
        document_models=[Family, User, Purchase]
    )