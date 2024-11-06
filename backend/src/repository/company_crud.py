from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from src.models.company import CompanyCreate, CompanyResponse, CompanyUpdate
from src.database.schemas import Company
from sqlalchemy.orm import joinedload


class CompanyCrudRepository:
    def __init__(self, database: AsyncSession) -> None:
        self.db: AsyncSession = database

    async def create(self, company: CompanyCreate) -> CompanyResponse:
        company_entity = Company(**company.dict())
        self.db.add(company_entity)
        await self.db.commit()
        await self.db.refresh(company_entity)
        return CompanyResponse.from_orm(company_entity)

    async def get_by_id(self, company_id: str) -> CompanyResponse:
        result = await self.db.execute(
            select(Company)
            .options(joinedload(Company.users), joinedload(Company.admin))
            .filter(Company.id == company_id)
        )
        company = result.unique().scalars().first()
        if not company:
            raise NoResultFound(f"Company with id {company_id} not found")
        return CompanyResponse.from_orm(company)

    async def get_by_email(self, contact_email: str) -> CompanyResponse | None:
        result = await self.db.execute(
            select(Company)
            .options(joinedload(Company.users), joinedload(Company.admin))
            .filter(Company.contact_email == contact_email)
        )
        company = result.unique().scalars().first()
        if not company:
            return None
        return CompanyResponse.from_orm(company)

    async def get_all(self) -> list[CompanyResponse]:
        result = await self.db.execute(
            select(Company).options(
                joinedload(Company.users), joinedload(Company.admin)
            )
        )
        companies = result.unique().scalars().all()
        return [CompanyResponse.from_orm(company) for company in companies]

    async def update(
        self, company_id: str, company_update: CompanyUpdate
    ) -> CompanyResponse:
        result = await self.db.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise NoResultFound(f"Company with id {company_id} not found")
        company_data = company_update.dict(exclude_unset=True)
        for key, value in company_data.items():
            setattr(company, key, value)
        await self.db.commit()
        await self.db.refresh(company)
        return CompanyResponse.from_orm(company)

    async def delete(self, company_id: str) -> bool:
        result = await self.db.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise NoResultFound(f"Company with id {company_id} not found")
        await self.db.delete(company)
        await self.db.commit()
        return True

    async def get_by_name(self, name: str) -> CompanyResponse | None:
        result = await self.db.execute(
            select(Company)
            .options(joinedload(Company.users), joinedload(Company.admin))
            .filter(Company.name == name)
        )
        company = result.unique().scalars().first()
        if not company:
            return None
        return CompanyResponse.from_orm(company)
