from app.repositories.family_repo import FamilyRepo
from app.repositories.transaction_repo import TransactionRepo
from app.schemas.family import FamilyCreate, FamilyUpdate, FamilyRead

class FamilyService:
    def __init__(self):
        self.repo = FamilyRepo()
        self.tx = TransactionRepo()

    async def create(self, data: FamilyCreate) -> FamilyRead:
        fam = await self.repo.create(data)
        return FamilyRead(
            id=str(fam.id),
            group_name=fam.group_name,
            tags=fam.tags,
            users=[],  # Инициализируем поле users как пустой список
            created_at=fam.created_at,
        )

    async def list(self) -> list[FamilyRead]:
        fams = await self.repo.list_all()
        out = []
        for f in fams:
            exp = await self.tx.sum_expenditure(str(f.id))
            out.append(FamilyRead(
                id=str(f.id),
                group_name=f.group_name,
                tags=f.tags,
                users=[str(u) for u in getattr(f, "users", [])],  # Инициализируем users как пустой список, если его нет
                created_at=f.created_at,
            ))
        return out

    async def get(self, fid: str) -> FamilyRead | None:
        f = await self.repo.get(fid)
        if not f:
            return None
        return FamilyRead(
            id=fid,
            group_name=f.group_name,
            tags=f.tags,
            users=[str(u) for u in f.users],  # Поле users возвращается
            created_at=f.created_at,
        )

    async def update(self, fid: str, data: FamilyUpdate) -> bool:
        return await self.repo.update(fid, data)

    async def delete(self, fid: str) -> bool:
        return await self.repo.delete(fid)