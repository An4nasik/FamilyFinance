from scr.models.family_models import Family, User, Purchase
from scr.database import init_db
import asyncio


async def main():
    await init_db()

    user = User(
        name="Антон",
        surname="Тайченачев",
        email="TaychenachevAA@stud.kai.ru",
        password="нет"
    )
    await user.insert()

    family = Family(
        group_name="Огузки",
        income=1000.00
    )
    await family.insert()

    await family.add_to_family(user)

    purchase = Purchase(
        price=1500.0,
        description="командно поели",
        user_id=user.id
    )
    await purchase.insert()
    await family.add_purchase(purchase)


if __name__ == "__main__":
    asyncio.run(main())