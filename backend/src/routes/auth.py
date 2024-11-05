from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.connection import get_db
from src.repository.user_crud import UserCrudRepository
from src.utils.jwt import create_access_token, create_refresh_token
from src.models.user import UserLogin
from src.utils.encrypter import verify_password
from src.models.token import TokenData
from src.utils.auth import RefreshTokenBearer


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
            token_data = TokenData(id=user.id, email=user.email, name=user.name)
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
                    "user": {"email": user.email, "name": user.name},
                },
                status_code=status.HTTP_200_OK,
            )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
    )


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
    )
