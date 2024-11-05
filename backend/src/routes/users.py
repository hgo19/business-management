from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from src.utils.auth import AccessTokenBearer, RoleChecker
from src.database.connection import get_db
from src.models.user import UserCreate, UserResponse, UserUpdate
from src.services.user_service import UserService
from src.repository.user_crud import UserCrudRepository
from src.services.company_service import CompanyService
from src.repository.company_crud import CompanyCrudRepository

user_router = APIRouter(prefix="/users", tags=["Users"])
access_token_bearer = AccessTokenBearer()

superadmin_checker = Depends(RoleChecker(["superadmin"]))
admin_checker = Depends(RoleChecker(["superadmin", "admin"]))


@user_router.post(
    "/company-admin",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[superadmin_checker],
)
async def create_company_admin(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db),
    token_details: dict = Depends(access_token_bearer),
):
    repository = UserCrudRepository(session)
    user_service = UserService(repository=repository)
    if user_data.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role must be admin for this endpoint",
        )

    if not user_data.company_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company ID is required for admin users",
        )

    new_user = await user_service.create_user(user_data)
    return new_user


@user_router.post(
    "/company-operator",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[admin_checker],
)
async def create_company_operator(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db),
    token_details: dict = Depends(access_token_bearer),
):
    if user_data.role != "operator":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role must be operator for this endpoint",
        )

    current_user = token_details.get("user")

    if current_user["role"] == "admin":
        if user_data.company_id != current_user["company_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin can only create operators for their own company",
            )

    if not user_data.company_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company ID is required for operator users",
        )

    user_repo = UserCrudRepository(session)
    comapny_repo = CompanyCrudRepository(session)
    company_service = CompanyService(comapny_repo)
    user_service = UserService(user_repo)

    new_user = await user_service.create_company_operator(user_data, company_service)
    return new_user


@user_router.get(
    "/company/{company_id}",
    response_model=List[UserResponse],
    dependencies=[admin_checker],
)
async def get_company_users(
    company_id: int,
    session: AsyncSession = Depends(get_db),
    token_details: dict = Depends(access_token_bearer),
):
    current_user = token_details.get("user")

    if current_user["role"] == "admin" and current_user["company_id"] != company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin can only view users from their own company",
        )

    repository = UserCrudRepository(session)
    user_service = UserService(repository=repository)

    users = await user_service.get_company_users(company_id)
    return users


@user_router.patch(
    "/{user_id}", response_model=UserResponse, dependencies=[admin_checker]
)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: AsyncSession = Depends(get_db),
    token_details: dict = Depends(access_token_bearer),
):
    current_user = token_details.get("user")

    repository = UserCrudRepository(session)
    user_service = UserService(repository=repository)

    user_to_update = await user_service.get_user_by_id(user_id)
    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if current_user["role"] == "admin":
        if user_to_update.company_id != current_user["company_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin can only update users from their own company",
            )
        if user_to_update.role != "operator" or user_update.role not in [
            None,
            "operator",
        ]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin can only update operators",
            )

    updated_user = await user_service.update_user(user_id, user_update)
    return updated_user


@user_router.delete(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[admin_checker]
)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_db),
    token_details: dict = Depends(access_token_bearer),
):
    current_user = token_details.get("user")

    repository = UserCrudRepository(session)
    user_service = UserService(repository=repository)

    user_to_delete = await user_service.get_user_by_id(user_id)
    if not user_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if current_user["role"] == "admin":
        if user_to_delete.company_id != current_user["company_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin can only delete users from their own company",
            )
        if user_to_delete.role != "operator":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin can only delete operators",
            )

    await user_service.delete_user(user_id)
    return {}
