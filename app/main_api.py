from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from models.family_models import Family, User, Purchase, pwd_context
from models.safe_family_models import SafeFamily, SafeUser, SafePurchase

router = APIRouter()


# Все эндпоинты
@router.get("/families", response_model=List[SafeFamily], tags=["Families"])
async def get_all_families():

        families = await Family.find_all().to_list()
        return [await prepare_family_response(family) for family in families]



@router.get("/families/{family_id}", response_model=SafeFamily, tags=["Families"])
async def get_family(family_id: str):
    try:
        family = await Family.get(ObjectId(family_id))
        if not family:
            raise HTTPException(404, detail="Family not found")
        return await prepare_family_response(family)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@router.get("/families/search/", response_model=SafeFamily, tags=["Families"])
async def search_family(group_name: str):
    try:
        family = await Family.find_one(Family.group_name == group_name)
        if not family:
            raise HTTPException(404, detail="Family not found")
        return await prepare_family_response(family)
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@router.get("/families/{family_id}/users", response_model=List[SafeUser], tags=["Users"])
async def get_family_users(family_id: str):
    try:
        family = await Family.get(ObjectId(family_id))
        if not family:
            raise HTTPException(404, detail="Family not found")

        users = []
        for user in family.users:
            user_doc = await User.get(user.id)
            users.append(SafeUser(
                id=str(user_doc.id),
                name=user_doc.name,
                surname=user_doc.surname,
                email=user_doc.email
            ))
        return users
    except Exception as e:
        raise HTTPException(500, detail=str(e))


@router.post("/families/{family_name}/users", tags=["Users"])
async def create_family_user(family_name: str, user_data: dict):

        # Найти семью
        family = await Family.find_one(Family.group_name == family_name)
        if not family:
            raise HTTPException(404, detail="Family not found")

        # Проверка существующего пользователя
        existing_user = await User.find_one(User.email == user_data["email"])
        if existing_user:
            raise HTTPException(400, detail="User already exists")

        # Создание пользователя
        new_user = User(
            name=user_data["name"],
            surname=user_data["surname"],
            email=user_data["email"],
            password=pwd_context.hash(user_data["password"])
        )
        await new_user.insert()

        # Добавление в семью
        await family.add_to_family(new_user)

        return {"status": "success", "user_id": str(new_user.id)}




@router.post("/families", tags=["Families"])
async def create_family(family_data: dict):
    try:
        existing_family = await Family.find_one(Family.group_name == family_data["group_name"])
        if existing_family:
            raise HTTPException(400, detail="Семья с таким названием уже существует")

        new_family = Family(
            group_name=family_data["group_name"],
            income=0,
            expenditure=0
        )
        await new_family.insert()
        return {"status": "success", "family_id": str(new_family.id)}

    except Exception as e:
        raise HTTPException(500, detail=str(e))

@router.post("/families/{family_name}/purchases", tags=["Purchases"])
async def create_family_purchase(family_name: str, purchase_data: dict):
    try:
        family = await Family.find_one(Family.group_name == family_name)
        if not family:
            raise HTTPException(404, detail="Family not found")

        user = await User.get(ObjectId(purchase_data["user_id"]))
        if not user:
            raise HTTPException(404, detail="User not found")

        new_purchase = Purchase(
            price=purchase_data["price"],
            description=purchase_data["description"],
            user_id=user.id
        )
        await new_purchase.insert()

        await family.add_purchase(new_purchase)
        return {"status": "success", "purchase_id": str(new_purchase.id)}

    except Exception as e:
        raise HTTPException(500, detail=str(e))


@router.get("/families/{family_id}/purchases", response_model=List[SafePurchase], tags=["Purchases"])
async def get_family_purchases(family_id: str):
    try:
        family = await Family.get(ObjectId(family_id))
        if not family:
            raise HTTPException(404, detail="Family not found")

        purchases = []
        for purchase in family.purchases:
            purchase_doc = await Purchase.get(purchase.id)
            user = await User.get(purchase_doc.user_id)
            purchases.append(SafePurchase(
                id=str(user.id),
                price=purchase_doc.price,
                description=purchase_doc.description,
                user_name=f"{user.name} {user.surname}"
            ))
        return purchases
    except Exception as e:
        raise HTTPException(500, detail=str(e))


# Вспомогательная функция
async def prepare_family_response(family: Family) -> SafeFamily:
    users = []
    for user in family.users:
        user_doc = await User.get(user.id)
        users.append(SafeUser(
            id=str(user.id),
            name=user_doc.name,
            surname=user_doc.surname,
            email=user_doc.email
        ))

    purchases = []
    for purchase in family.purchases:
        purchase_doc = await Purchase.get(purchase.id)
        user = await User.get(purchase_doc.user_id)
        purchases.append(SafePurchase(
            id=str(user.id),
            price=purchase_doc.price,
            description=purchase_doc.description,
            user_name=f"{user.name} {user.surname}" if user else "Unknown"
        ))

    return SafeFamily(
        id=str(family.id),
        group_name=family.group_name,
        total_balance=family.income - family.expenditure,
        users_count=len(users),
        expenditure=family.expenditure,
        income=family.income,
        users=users,
        purchases=purchases
    )