from passlib.context import CryptContext
from pymongo import MongoClient

from scr.schemas.family_scheme import Family, User, Purchase

client = MongoClient("localhost", port=27017)
families_db =  client["family_db"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



family = Family(
    group_name="Тестовая",
    )
user = User(
    name="Антон",
    surname="Тайченачев",
    email="TaychenachevAA@stud.kai.ru",
    password=pwd_context.hash("нет")
)
purchase = Purchase(
    price=1000.0,
    description="Тестовая закупка",
    user_id=user.id
)
families_db["users"].insert_one(user.model_dump(by_alias=True))
families_db["families"].insert_one(family.model_dump(by_alias=True))
family.add_to_family(user)
family.add_purchase(purchase)