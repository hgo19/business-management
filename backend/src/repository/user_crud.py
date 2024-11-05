from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from ..models.user import UserCreate, UserRead
from ..database.schemas import User


class UserCrudRepository:
    def __init__(self, database: AsyncSession) -> None:
        self.db: AsyncSession = database

    async def create(self, user: UserCreate) -> UserRead:
        user_entity = User(**user.dict())
        self.db.add(user_entity)
        await self.db.commit()
        await self.db.refresh(user_entity)
        return UserRead.from_orm(user_entity)

    async def get_by_id(self, user_id: str) -> UserRead:
        result = await self.db.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if not user:
            raise NoResultFound(f"User with id {user_id} not found")
        return UserRead.from_orm(user)

    async def get_by_email(self, email: str) -> UserRead | None:
        result = await self.db.execute(select(User).filter(User.email == email))
        user = result.scalars().first()
        if not user:
            return None
        return UserRead.from_orm(user)

    async def get_all(self) -> list[UserRead]:
        result = await self.db.execute(select(User))
        users = result.scalars().all()
        return [UserRead.from_orm(user) for user in users]

    async def update(self, user_id: str, user_update: UserCreate) -> UserRead:
        result = await self.db.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if not user:
            raise NoResultFound(f"User with id {user_id} not found")

        user_data = user_update.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)

        await self.db.commit()
        await self.db.refresh(user)
        return UserRead.from_orm(user)
