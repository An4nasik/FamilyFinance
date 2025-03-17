from pymongo import MongoClient
from pydantic import SecretStr, EmailStr
from schemas.family_scheme import User, Family, pwd_context, Purchase
from scr.schemas.family_scheme import Family

client = MongoClient("localhost", port=27017)
families_db =  client["family_db"]
user_data = {
    "id": 1,
    "name": "Anton",
    "surname": "Taychenachev",
    "email": "TaychenachevAA@stud.kai.ru",
    "password": "нет"
}
family = Family(
    group_name="Тестовая"
)
user = User(
    name=user_data["name"],
    surname=user_data["surname"],
    email=user_data["email"],
    password=pwd_context.hash(user_data["password"])
)
families_db["users"].insert_one(user.model_dump(by_alias=True))
families_db["families"].insert_one(family.model_dump(by_alias=True))
family.add_to_family(user)
family = families_db["families"].find_one({})
family = Family(**family)
purchase = Purchase(
    price=1000,
    description="Я зОхотел пива",
    user_id=family.users[0].id
)
purchase2 = Purchase(
    price=1000,
    description="Я зОхотел пива",
    user_id=family.users[0].id
)
print(family.add_purchase(purchase2))
print(family.add_purchase(purchase))





