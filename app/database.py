from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.family_models import Family, User, Purchase

async def init_db():
    # Connect to MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    # Initialize Beanie with the database and models
    await init_beanie(database=client["family_finance_db"], document_models=[Family, User, Purchase])