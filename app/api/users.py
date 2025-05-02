from fastapi import APIRouter, HTTPException
from typing import List
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/families/{family_id}/users", tags=["Users"])
service = UserService()

@router.get("", response_model=List[UserRead])
async def list_users(family_id: str):
    return await service.list(family_id)

@router.post("", status_code=201)
async def add_user(family_id: str, data: UserCreate):
    return await service.add(family_id, data)

@router.delete("/{user_id}")
async def remove_user(family_id: str, user_id: str):
    ok = await service.remove(user_id)
    if not ok:
        raise HTTPException(404, "User not found")
    return {"status": "success"}