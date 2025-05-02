from fastapi import APIRouter, HTTPException
from typing import List
from app.services.family_service import FamilyService
from app.schemas.family import FamilyCreate, FamilyRead, FamilyUpdate

router = APIRouter(prefix="/families", tags=["Families"])
service = FamilyService()

@router.get("", response_model=List[FamilyRead])
async def list_families():
    return await service.list()

@router.get("/{family_id}", response_model=FamilyRead)
async def get_family(family_id: str):
    res = await service.get(family_id)
    if not res:
        raise HTTPException(404, "Family not found")
    return res

@router.post("", status_code=201)
async def create_family(data: FamilyCreate):
    return await service.create(data)

@router.put("/{family_id}")
async def update_family(family_id: str, data: FamilyUpdate):
    ok = await service.update(family_id, data)
    if not ok:
        raise HTTPException(404, "Family not found or no fields to update")
    return {"status": "success"}

@router.delete("/{family_id}")
async def delete_family(family_id: str):
    ok = await service.delete(family_id)
    if not ok:
        raise HTTPException(404, "Family not found")
    return {"status": "success"}