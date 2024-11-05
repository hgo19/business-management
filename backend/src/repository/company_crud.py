from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from src.models.company import CompanyCreate, CompanyRead, CompanyUpdate
from src.database.schemas import Company


class CompanyCrudRepository:
    def __init__(self, database: AsyncSession) -> None:
        self.db: AsyncSession = database

    async def create(self, company: CompanyCreate) -> CompanyRead:
        company_entity = Company(**company.dict())
        self.db.add(company_entity)
        await self.db.commit()
        await self.db.refresh(company_entity)
        return CompanyRead.from_orm(company_entity)

    async def get_by_id(self, company_id: str) -> CompanyRead:
        result = await self.db.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise NoResultFound(f"Company with id {company_id} not found")
        return CompanyRead.from_orm(company)

    async def get_by_email(self, contact_email: str) -> CompanyRead | None:
        result = await self.db.execute(
            select(Company).filter(Company.contact_email == contact_email)
        )
        company = result.scalars().first()
        if not company:
            return None
        return CompanyRead.from_orm(company)

    async def get_all(self) -> list[CompanyRead]:
        result = await self.db.execute(select(Company))
        companies = result.scalars().all()
        return [CompanyRead.from_orm(company) for company in companies]

    async def update(self, company_id: str, company_update: CompanyUpdate) -> CompanyRead:
        result = await self.db.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise NoResultFound(f"Company with id {company_id} not found")

        company_data = company_update.dict(exclude_unset=True)
        for key, value in company_data.items():
            setattr(company, key, value)

        await self.db.commit()
        await self.db.refresh(company)
        return CompanyRead.from_orm(company)

    async def delete(self, company_id: str) -> None:
        result = await self.db.execute(select(Company).filter(Company.id == company_id))
        company = result.scalars().first()
        if not company:
            raise NoResultFound(f"Company with id {company_id} not found")
            
        await self.db.delete(company)
        await self.db.commit()

    async def get_by_name(self, name: str) -> CompanyRead | None:
        result = await self.db.execute(select(Company).filter(Company.name == name))
        company = result.scalars().first()
        if not company:
            return None
        return CompanyRead.from_orm(company)