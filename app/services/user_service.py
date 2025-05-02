from app.repositories.user_repo import UserRepo
from app.schemas.user import UserCreate, UserRead
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self):
        self.repo = UserRepo()

    async def add(self, fid: str, data: UserCreate) -> UserRead:
        data.password = pwd_context.hash(data.password)
        u = await self.repo.create(fid, data)
        return UserRead(
            id=str(u.id),
            name=u.name,
            email=u.email,
            created_at=u.created_at,
        )

    async def list(self, fid: str) -> list[UserRead]:
        us = await self.repo.list_by_family(fid)
        return [UserRead(
            id=str(u.id),
            name=u.name,
            email=u.email,
            created_at=u.created_at
        ) for u in us]

    async def remove(self, uid: str) -> bool:
        return await self.repo.delete(uid)