from typing import List, Optional
from bson import ObjectId as BsonObjectId
from beanie import Document
from passlib.context import CryptContext
from pydantic import Field, EmailStr

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Custom ObjectId type with validation

class ObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info):
        if isinstance(v, str):
            try:
                return cls(v)
            except Exception:
                raise ValueError("Invalid ObjectId")
        if isinstance(v, BsonObjectId):
            return v
        raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_json_schema__(cls, schema):
        # Define the JSON schema for ObjectId
        schema.update({"type": "string", "format": "objectid"})
        return schema

class Config:
    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
        "loc_by_alias": True,
    }

class User(Document, Config):
    id: ObjectId = Field(default_factory=BsonObjectId, alias="_id")
    name: str
    surname: str
    email: EmailStr
    password: str
    group_id: Optional[ObjectId] = None

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)

    class Settings:
        name = "users"

class Purchase(Document, Config):
    id: ObjectId = Field(default_factory=BsonObjectId, alias="_id")
    price: float
    description: str
    user_id: ObjectId

    class Settings:
        name = "purchases"

class Family(Document, Config):
    id: ObjectId = Field(default_factory=BsonObjectId, alias="_id")
    group_name: str
    users: List[User] = Field(default_factory=list)
    expenditure: float = 0
    income: float = 0
    purchases: List[Purchase] = Field(default_factory=list)

    @property
    async def users_count(self) -> int:
        return len(self.users)

    async def add_to_family(self, user: User) -> None:
        user.group_id = self.id
        self.users.append(user)
        await self.save()
        await user.save()

    async def add_purchase(self, purchase: Purchase) -> None:
        self.purchases.append(purchase)
        self.expenditure += purchase.price
        await self.save()

    class Settings:
        name = "families"