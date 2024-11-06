from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from ..models.user import UserCreate, UserResponse, UserUpdate, UserRead
from ..database.schemas import User, Roles
from sqlalchemy.dialects.postgresql import dialect

class UserCrudRepository:
    def __init__(self, database: AsyncSession) -> None:
        self.db: AsyncSession = database

    async def create(self, user: UserCreate) -> UserResponse:
        user_entity = User(**user.dict())
        self.db.add(user_entity)
        await self.db.commit()
        await self.db.refresh(user_entity)
        return UserResponse.from_orm(user_entity)

    async def get_by_id(self, user_id: str) -> UserResponse:
        result = await self.db.execute(
            select(User)
            .options(
                joinedload(User.company),
                joinedload(User.administered_companies)
            )
            .filter(User.id == user_id)
        )
        user = result.unique().scalars().first()
        if not user:
            raise NoResultFound(f"User with id {user_id} not found")
        return UserResponse.from_orm(user)

    async def get_by_email(self, email: str) -> UserRead | None:
        result = await self.db.execute(
            select(User)
            .options(
                joinedload(User.company),
                joinedload(User.administered_companies)
            )
            .filter(User.email == email)
        )
        user = result.unique().scalars().first()
        if not user:
            return None
        return UserRead.from_orm(user)

    async def get_all(self) -> list[UserResponse]:
        result = await self.db.execute(
            select(User)
            .options(
                joinedload(User.company),
                joinedload(User.administered_companies)
            )
        )


        users = result.unique().scalars().all()
        return [UserResponse.from_orm(user) for user in users]

    async def update(self, user_id: str, user_update: UserUpdate) -> UserResponse:
        result = await self.db.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if not user:
            raise NoResultFound(f"User with id {user_id} not found")
        user_data = user_update.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)
        await self.db.commit()
        await self.db.refresh(user)
        return UserResponse.from_orm(user)

    async def delete(self, user_id: str) -> bool:
        result = await self.db.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if not user:
            raise NoResultFound(f"User with id {user_id} not found")
        await self.db.delete(user)
        await self.db.commit()
        return True

    async def get_by_company_id(self, company_id: str) -> list[UserResponse]:
        result = await self.db.execute(
            select(User)
            .options(
                joinedload(User.company),
                joinedload(User.administered_companies)
            )
            .filter(User.company_id == company_id)
        )
        users = result.unique().scalars().all()
        return [UserResponse.from_orm(user) for user in users]

    async def get_all_admins(self) -> list[UserResponse]:
        result = await self.db.execute(
            select(User)
            .options(
                joinedload(User.company),
                joinedload(User.administered_companies)
            )
            .filter(User.role == Roles.admin)
        )
        users = result.unique().scalars().all()
        return [UserResponse.from_orm(user) for user in users]
