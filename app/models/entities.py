from typing import List
from datetime import datetime
from bson import ObjectId
from pydantic import Field
from app.models.base import BaseModel

class Family(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    group_name: str
    tags: List[str] = []
    users: List[ObjectId] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

class User(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    name: str
    email: str
    password: str
    group_id: ObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Transaction(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    user_id: ObjectId
    amount: float
    tags: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)