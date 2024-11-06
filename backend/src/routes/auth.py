from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.connection import get_db
from src.repository.user_crud import UserCrudRepository
from src.utils.jwt import create_access_token, create_refresh_token
from src.models.user import UserLogin, UserResponse
from src.utils.encrypter import verify_password
from src.models.token import TokenData, TokenResponse
from src.utils.auth import RefreshTokenBearer, get_current_user


auth_router = APIRouter(prefix="/auth", tags=["Auth"])

REFRESH_TOKEN_EXPIRY = 3


@auth_router.post("/login")
async def login_users(login_data: UserLogin, session: AsyncSession = Depends(get_db)):
    email = login_data.email
    password = login_data.password
    user_repository = UserCrudRepository(session)

    user = await user_repository.get_by_email(email)

    if user is not None:
        password_valid = verify_password(password, hashed_password=user.password)

        if password_valid:
            token_data = TokenData(
                id=user.id, email=user.email, name=user.name, role=user.role
            )
            access_token = create_access_token(data=token_data)

            refresh_token = create_refresh_token(
                token_data,
                expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": jsonable_encoder(user),
                },
                status_code=status.HTTP_200_OK,
            )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
    )


@auth_router.post("/refresh_token")
async def get_new_access_token(
    token_details: TokenResponse = Depends(RefreshTokenBearer()),
):
    expiry_timestamp = token_details.exp
    token_dict = token_details.dict()
    token_dict.pop("token", None)
    token_data = TokenData(**token_dict)

    if expiry_timestamp > datetime.now(timezone.utc):
        new_access_token = create_access_token(token_data)

        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
    )


@auth_router.get("/me")
async def read_current_user(current_user: UserResponse = Depends(get_current_user)):
    return current_user
