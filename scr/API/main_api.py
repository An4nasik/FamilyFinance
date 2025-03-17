from typing import List
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from pymongo import MongoClient

main_api_router = APIRouter()

# Подключение к MongoDB
client = MongoClient("localhost", port=27017)
db = client["family_db"]

class SafeUser(BaseModel):
    name: str
    surname: str
    email: str

class SafePurchase(BaseModel):
    price: float
    description: str
    user_name: str

class SafeFamily(BaseModel):
    group_name: str
    created_at: str
    total_balance: float
    users_count: int
    expenditure: float
    income: float
    users: List[SafeUser]
    purchases: List[SafePurchase]

def prepare_family_response(family_data: dict) -> SafeFamily:
    users = []
    purchases = []

    # Обработка пользователей
    for user_ref in family_data.get("users", []):
        user = db["users"].find_one({"_id": user_ref["_id"]})
        if user:
            users.append(SafeUser(
                name=user["name"],
                surname=user["surname"],
                email=user["email"]
            ))

    # Обработка покупок
    for purchase in family_data.get("purchases", []):
        user = db["users"].find_one({"_id": purchase["user_id"]})
        purchases.append(SafePurchase(
            price=purchase["price"],
            description=purchase["description"],
            user_name=f"{user['name']} {user['surname']}" if user else "none"
        ))

    # Новые поля
    created_at = family_data["_id"].generation_time.strftime("%d.%m.%Y в %H:%M")
    total_balance = family_data.get("income", 0) - family_data.get("expenditure", 0)

    return SafeFamily(
        group_name=family_data["group_name"],
        created_at=created_at,
        total_balance=total_balance,
        users_count=len(users),
        expenditure=family_data.get("expenditure", 0),
        income=family_data.get("income", 0),
        users=users,
        purchases=purchases
    )

@main_api_router.get("/families", response_model=List[SafeFamily], tags=["Families"])
async def get_all_families():
    try:
        families = list(db["families"].find())
        return [prepare_family_response(f) for f in families]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@main_api_router.get("/families/{family_id}", response_model=SafeFamily, tags=["Families"])
async def get_family(family_id: str):
    try:
        family_data = db["families"].find_one({"_id": ObjectId(family_id)})
        if not family_data:
            raise HTTPException(status_code=404, detail="Family not found")
        return prepare_family_response(family_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@main_api_router.get("/families/search/", response_model=SafeFamily, tags=["Families"])
async def search_family(group_name: str):
    try:
        family_data = db["families"].find_one({"group_name": group_name})
        if not family_data:
            raise HTTPException(status_code=404, detail="Family not found")
        return prepare_family_response(family_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@main_api_router.get("/families/{family_id}/users", response_model=List[SafeUser], tags=["Users"])
async def get_family_users(family_id: str):
    try:
        family = db["families"].find_one({"_id": ObjectId(family_id)})
        if not family:
            raise HTTPException(status_code=404, detail="Family not found")

        users = []
        for user_ref in family.get("users", []):
            user = db["users"].find_one({"_id": user_ref["_id"]})
            if user:
                users.append(SafeUser(**{
                    "name": user["name"],
                    "surname": user["surname"],
                    "email": user["email"]
                }))
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@main_api_router.get("/families/{family_id}/purchases", response_model=List[SafePurchase], tags=["Purchases"])
async def get_family_purchases(family_id: str):
    try:
        family = db["families"].find_one({"_id": ObjectId(family_id)})
        if not family:
            raise HTTPException(status_code=404, detail="Family not found")

        purchases = []
        for purchase in family.get("purchases", []):
            user = db["users"].find_one({"_id": purchase["user_id"]})
            purchases.append(SafePurchase(
                price=purchase["price"],
                description=purchase["description"],
                user_name=f"{user['name']} {user['surname']}" if user else "Unknown"
            ))
        return purchases
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


