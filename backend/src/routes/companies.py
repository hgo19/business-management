from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.auth import AccessTokenBearer, RoleChecker, get_current_user
from src.database.connection import get_db
from src.models.company import CompanyCreate, CompanyRead, CompanyUpdate
from src.services.company_service import CompanyService
from src.repository.company_crud import CompanyCrudRepository
from src.services.user_service import UserService
from src.repository.user_crud import UserCrudRepository
from src.models.user import UserRead

company_router = APIRouter(prefix="/companies", tags=["Companies"])
access_token_bearer = AccessTokenBearer()

superadmin_checker = Depends(RoleChecker(["superadmin"]))
admin_checker = Depends(RoleChecker(["superadmin", "admin"]))


@company_router.post(
    "/",
    response_model=CompanyRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[superadmin_checker],
)
async def create_company(
    company_data: CompanyCreate,
    session: AsyncSession = Depends(get_db),
    token_details: dict = Depends(access_token_bearer),
):
    user_repo = UserCrudRepository(session)
    user_service = UserService(repository=user_repo)
    company_repo = CompanyCrudRepository(session)
    company_service = CompanyService(repository=company_repo)

    admin_user = await user_service.get_user_by_id(company_data.admin_id)

    if not admin_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin")

    try:
        new_company = await company_service.create_company(company_data, admin_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return new_company


@company_router.get(
    "/{company_id}",
    response_model=CompanyRead,
    dependencies=[admin_checker],
)
async def get_company_by_id(
    company_id: int,
    session: AsyncSession = Depends(get_db),
    token_details: dict = Depends(access_token_bearer),
):
    current_user = token_details.get("user")
    repository = CompanyCrudRepository(session)
    company_service = CompanyService(repository=repository)

    company = await company_service.get_company_by_id(company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    if current_user["role"] == "admin" and current_user["company_id"] != company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin can only view their own company",
        )

    return company


@company_router.get(
    "/",
    response_model=List[CompanyRead],
    dependencies=[superadmin_checker],
)
async def get_all_companies(
    session: AsyncSession = Depends(get_db),
):
    repository = CompanyCrudRepository(session)
    company_service = CompanyService(repository=repository)
    companies = await company_service.get_all_companies()
    return companies


@company_router.patch(
    "/{company_id}",
    response_model=CompanyRead,
    dependencies=[admin_checker],
)
async def update_company(
    company_id: int,
    company_update: CompanyUpdate,
    session: AsyncSession = Depends(get_db),
    token_details: dict = Depends(access_token_bearer),
):
    current_user = token_details.get("user")
    repository = CompanyCrudRepository(session)
    company_service = CompanyService(repository=repository)

    existing_company = await company_service.get_company_by_id(company_id)
    if not existing_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    if current_user["role"] == "admin" and current_user["company_id"] != company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin can only update their own company",
        )

    is_valid_update = await company_service.validate_company_update(company_id, company_update)
    if not is_valid_update:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid company update")

    updated_company = await company_service.update_company(company_id, company_update)
    return updated_company


@company_router.delete(
    "/{company_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[superadmin_checker],
)
async def delete_company(
    company_id: int,
    session: AsyncSession = Depends(get_db),
    token_details: dict = Depends(access_token_bearer),
):
    repository = CompanyCrudRepository(session)
    company_service = CompanyService(repository=repository)

    existing_company = await company_service.get_company_by_id(company_id)
    if not existing_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    await company_service.delete_company(company_id)
    return {}


@company_router.get(
    "/me",
    response_model=CompanyRead,
    dependencies=[Depends(access_token_bearer)],
)
async def get_my_company(
    session: AsyncSession = Depends(get_db),
    current_user: UserRead = Depends(get_current_user),
):

    if not current_user.company_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not belong to any company",
        )

    repository = CompanyCrudRepository(session)
    company_service = CompanyService(repository=repository)

    company = await company_service.get_company_by_id(current_user["company_id"])
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    return company
