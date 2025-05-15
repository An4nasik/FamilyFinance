from app.repositories.transaction_repo import TransactionRepo
from app.schemas.transaction import PurchaseCreate, TopUpCreate, OperationRead

class TransactionService:
    def __init__(self):
        self.repo = TransactionRepo()

    async def list(self, fid: str) -> list[OperationRead]:
        ops = await self.repo.list_by_family(fid)
        return [
            OperationRead(
                id=str(o.id),
                user_id=str(o.user_id),
                amount=o.amount,
                tags=o.tags,
                date=o.date,
                created_at=o.created_at,
            )
            for o in ops
        ]

    async def purchase(self, family_id: str, data: PurchaseCreate):
        t = await self.repo.create_purchase(data, family_id)
        return {
            "purchase_id": str(t.id),
            "date": t.date
        }

    async def topup(self, family_id: str, data: TopUpCreate):
        t = await self.repo.create_topup(data, family_id)
        return {
            "topup_id": str(t.id),
              "date": t.date}

    async def remove(self, tid: str) -> bool:
        return await self.repo.delete(tid)