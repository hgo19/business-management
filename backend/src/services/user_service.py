from src.models.user import UserCreate, UserRead, UserUpdate
from src.repository.user_crud import UserCrudRepository
from src.utils.encrypter import hash_password
from .company_service import CompanyService


class UserService:
    def __init__(self, repository: UserCrudRepository) -> None:
        self.repository = repository

    async def create_user(self, user_create: UserCreate) -> UserRead:
        user_create.password = hash_password(user_create.password)
        return await self.repository.create(user_create)

    async def get_user_by_id(self, user_id: str) -> UserRead:
        return await self.repository.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> UserRead | None:
        return await self.repository.get_by_email(email)

    async def get_all_users(self) -> list[UserRead]:
        return await self.repository.get_all()

    async def get_all_admins(self) -> list[UserRead]:
        return await self.repository.get_all_admins()

    async def update_user(self, user_id: str, user_update: UserUpdate) -> UserRead:
        if user_update.password:
            user_update.password = hash_password(user_update.password)
        return await self.repository.update(user_id, user_update)

    async def delete_user(self, user_id: str) -> None:
        await self.repository.delete(user_id)

    async def get_company_users(self, company_id: str) -> list[UserRead]:
        return await self.repository.get_by_company_id(company_id)

    async def validate_company_operator(
        self, user_data: UserCreate, company_service: CompanyService
    ) -> bool:
        return await company_service.validate_company_exists(user_data.company_id)

    async def create_company_operator(
        self, user_data: UserCreate, company_service: CompanyService
    ) -> UserRead:
        company_id = user_data.company_id
        if await self.validate_company_operator(user_data, company_service, company_id):
            return await self.create_user(user_data)
        raise ValueError("Invalid company or operator creation parameters")
