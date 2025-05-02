from datetime import datetime
from typing import List
from pydantic import BaseModel

class FamilyCreate(BaseModel):
    group_name: str
    tags: List[str] = []

class FamilyRead(BaseModel):
    id: str
    group_name: str
    tags: List[str]
    users_count: int
    total_expenditure: float
    created_at: datetime

class FamilyUpdate(BaseModel):
    group_name: str | None = None
    tags: List[str] | None = None