from src.models.company import CompanyCreate, CompanyRead, CompanyUpdate
from src.models.user import UserRead
from src.repository.company_crud import CompanyCrudRepository
from sqlalchemy.exc import NoResultFound
from src.services.user_service import UserService


class CompanyService:
    def __init__(self, repository: CompanyCrudRepository) -> None:
        self.repository = repository

    async def create_company(
        self,
        company_create: CompanyCreate,
        admin_user_id: str,
        user_service: UserService,
    ) -> CompanyRead:
        admin_user = await user_service.get_user_by_id(admin_user_id)
        if not admin_user:
            raise ValueError("An admin user is required to create a company.")
        existing_company = await self.repository.get_by_email(
            company_create.contact_email
        )
        if existing_company:
            raise ValueError("Company with this email already exists")
        return await self.repository.create(company_create)

    async def get_company_by_id(self, company_id: str) -> CompanyRead:
        return await self.repository.get_by_id(company_id)

    async def get_company_by_email(self, email: str) -> CompanyRead | None:
        return await self.repository.get_by_email(email)

    async def get_all_companies(self) -> list[CompanyRead]:
        return await self.repository.get_all()

    async def update_company(
        self, company_id: str, company_update: CompanyUpdate
    ) -> CompanyRead:
        return await self.repository.update(company_id, company_update)

    async def delete_company(self, company_id: str) -> None:
        await self.repository.delete(company_id)

    async def get_company_by_name(self, name: str) -> CompanyRead | None:
        return await self.repository.get_by_name(name)

    async def validate_company_exists(self, company_id: str) -> bool:
        try:
            await self.get_company_by_id(company_id)
            return True
        except NoResultFound:
            return False

    async def validate_company_creation(self, company_create: CompanyCreate) -> bool:
        existing_company = await self.get_company_by_email(company_create.contact_email)
        if existing_company:
            return False
        existing_company = await self.get_company_by_name(company_create.name)
        if existing_company:
            return False
        return True

    async def validate_company_update(
        self, company_id: str, company_update: CompanyUpdate
    ) -> bool:
        try:
            existing_company = await self.get_company_by_id(company_id)
            if (
                company_update.contact_email
                and company_update.contact_email != existing_company.contact_email
            ):
                email_exists = await self.get_company_by_email(
                    company_update.contact_email
                )
                if email_exists:
                    return False
            if company_update.name and company_update.name != existing_company.name:
                name_exists = await self.get_company_by_name(company_update.name)
                if name_exists:
                    return False
            return True
        except NoResultFound:
            return False

    async def validate_user_company_association(
        self, user_data: UserRead, admin_company_id: str | None = None
    ) -> bool:
        if not user_data.company_id:
            return True
        company_exists = await self.validate_company_exists(user_data.company_id)
        if not company_exists:
            return False
        if admin_company_id:
            admin_company_exists = await self.validate_company_exists(admin_company_id)
            if not admin_company_exists:
                return False
        return True
