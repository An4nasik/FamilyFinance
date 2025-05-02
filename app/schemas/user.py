from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: datetime