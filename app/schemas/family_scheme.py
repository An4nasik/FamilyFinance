from pydantic import BaseModel, ConfigDict, EmailStr, Field
from bson import ObjectId
from typing import List
from pymongo import MongoClient
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
client = MongoClient("localhost", port=27017)
families_db =  client["family_db"]


class Config:
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True)


class User(BaseModel, Config):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    name: str
    surname: str
    email: EmailStr
    password: str
    group_id: ObjectId = None

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)



class Purchase(BaseModel, Config):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    price: float
    description: str
    user_id: ObjectId


class Family(BaseModel, Config):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    group_name: str
    users: List[User] = Field(default_factory=list)
    expenditure: float = 0
    income: float = 0
    purchases: List[Purchase] = Field(default_factory=list)

    @property
    def users_count(self) -> int:
        return len(self.users)

    def add_to_family(self, user: User) -> list:
        user.group_id = self.id
        self.users.append(user)
        operations = [families_db["families"].update_one(
            {"_id": self.id},
            {"$set": self.model_dump()},
            upsert=True
        ), families_db["users"].update_one(
            {"email": user.email},
            {"$set": user.model_dump()},
            upsert=True
        )]
        return operations

    def add_purchase(self, purchase: Purchase) -> list:
        self.purchases.append(purchase)
        self.expenditure += purchase.price
        operations = [
            families_db["families"].update_one(
                {"_id": self.id},
                {"$set": self.model_dump(by_alias=True)},
                upsert=False
            )
        ]
        return operations

