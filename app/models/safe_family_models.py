from typing import List
from pydantic import BaseModel, EmailStr, ConfigDict


class Config:
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        loc_by_alias=True)


class SafeUser(BaseModel, Config):
    id: str
    name: str
    surname: str
    email: EmailStr


class SafePurchase(BaseModel, Config):
    id: str
    price: float
    description: str
    user_name: str


class SafeFamily(BaseModel, Config):
    id: str
    group_name: str
    total_balance: float
    users_count: int
    expenditure: float
    income: float
    users: List[SafeUser]
    purchases: List[SafePurchase]