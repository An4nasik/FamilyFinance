from bson import ObjectId
from app.database import mongodb
from app.models.entities import User
from app.schemas.user import UserCreate

class UserRepo:
    coll = mongodb.coll("users")

    async def create(self, fid: str, data: UserCreate) -> User:
        u = User(**data.model_dump(), group_id=ObjectId(fid))
        await self.coll.insert_one(u.model_dump(by_alias=True))
        return u

    async def list_by_family(self, fid: str) -> list[User]:
        cursor = self.coll.find({"group_id": ObjectId(fid)})
        return [User(**doc) async for doc in cursor]

    async def delete(self, uid: str) -> bool:
        res = await self.coll.delete_one({"_id": ObjectId(uid)})
        return res.deleted_count > 0