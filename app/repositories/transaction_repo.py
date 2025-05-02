from bson import ObjectId
from app.database import mongodb
from app.models.entities import Transaction
from app.schemas.transaction import PurchaseCreate, TopUpCreate

class TransactionRepo:
    coll = mongodb.coll("transactions")

    async def list_by_family(self, fid: str) -> list[Transaction]:
        pipeline = [
            {"$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user"
            }},
            {"$unwind": "$user"},
            {"$match": {"user.group_id": ObjectId(fid)}}
        ]
        docs = await self.coll.aggregate(pipeline).to_list(None)
        return [Transaction(**doc) for doc in docs]

    async def create_purchase(self, data: PurchaseCreate) -> Transaction:
        t = Transaction(**data.model_dump(), amount=-abs(data.price))
        await self.coll.insert_one(t.model_dump(by_alias=True))
        return t

    async def create_topup(self, data: TopUpCreate) -> Transaction:
        t = Transaction(**data.model_dump(), amount=abs(data.amount))
        await self.coll.insert_one(t.model_dump(by_alias=True))
        return t

    async def delete(self, tid: str) -> bool:
        res = await self.coll.delete_one({"_id": ObjectId(tid)})
        return res.deleted_count > 0

    async def sum_expenditure(self, fid: str) -> float:
        pipeline = [
            {"$lookup": {"from":"users","localField":"user_id","foreignField":"_id","as":"u"}},
            {"$unwind":"$u"},
            {"$match":{"u.group_id":ObjectId(fid)}},
            {"$group":{"_id":None,"sum":{"$sum":"$amount"}}}
        ]
        r = await self.coll.aggregate(pipeline).to_list(1)
        return r[0]["sum"] if r else 0.0