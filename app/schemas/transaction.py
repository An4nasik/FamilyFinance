from datetime import datetime, date
from typing import List
from pydantic import field_validator
from app.models.base import BaseModel

class PurchaseCreate(BaseModel):
    user_id: str
    price: float
    tags: List[str] = []
    date: str  # Изменено с date на str

    @field_validator("date")
    def validate_date(cls, v):
        try:
            datetime.strptime(v, "%d.%m.%Y")  # Проверяем формат ДД.ММ.ГГГГ
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        return v

class TopUpCreate(BaseModel):
    user_id: str
    amount: float
    tags: List[str] = []
    date: str  # Изменено с date на str

    @field_validator("date")
    def validate_date(cls, v):
        try:
            datetime.strptime(v, "%d.%m.%Y")  # Проверяем формат ДД.ММ.ГГГГ
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        return v

class OperationRead(BaseModel):
    id: str
    user_id: str
    amount: float
    tags: List[str]
    date: str  # Изменено с date на str
    created_at: datetime