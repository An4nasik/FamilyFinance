from typing import Optional
from bson import ObjectId
from app.database import mongodb
from app.models.entities import Family
from app.schemas.family import FamilyCreate, FamilyUpdate

class FamilyRepo:
    coll = mongodb.coll("families")

    async def create(self, data: FamilyCreate) -> Family:
        doc = Family(**data.model_dump())
        await self.coll.insert_one(doc.model_dump(by_alias=True))
        return doc

    async def get(self, fid: str) -> Optional[Family]:
        j = await self.coll.find_one({"_id": ObjectId(fid)})
        return Family(**j) if j else None

    async def list_all(self) -> list[Family]:
        cursor = self.coll.find()
        return [Family(**doc) async for doc in cursor]

    async def update(self, fid: str, data: FamilyUpdate) -> bool:
        upd = {k: v for k, v in data.model_dump().items() if v is not None}
        if not upd:
            return False
        res = await self.coll.update_one({"_id": ObjectId(fid)}, {"$set": upd})
        return res.modified_count > 0

    async def delete(self, fid: str) -> bool:
        res = await self.coll.delete_one({"_id": ObjectId(fid)})
        return res.deleted_count > 0