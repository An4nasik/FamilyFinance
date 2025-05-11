from typing import List
from datetime import datetime
from bson import ObjectId
from pydantic import Field
from app.models.base import BaseModel
from datetime import date

BASE_TAGS = ["еда", "транспорт", "развлечения", "досуг", "другое"]

class Family(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    group_name: str
    tags: List[str] = []
    users: List[ObjectId] = []  # Поле users инициализируется как пустой список
    created_at: datetime = Field(default_factory=datetime.now)

class User(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    name: str
    email: str
    password: str
    group_id: ObjectId
    created_at: datetime = Field(default_factory=datetime.now)

class Transaction(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    user_id: ObjectId
    amount: float
    tags: List[str] = BASE_TAGS
    date: str
    created_at: datetime = Field(default_factory=datetime.now)
