from datetime import datetime
from typing import List
from pydantic import BaseModel

class PurchaseCreate(BaseModel):
    user_id: str
    price: float
    tags: List[str] = []

class TopUpCreate(BaseModel):
    user_id: str
    amount: float
    tags: List[str] = []

class OperationRead(BaseModel):
    id: str
    user_id: str
    amount: float
    tags: List[str]
    created_at: datetime