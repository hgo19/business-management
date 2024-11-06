from typing import Optional
from pydantic import Field, validator, BaseModel, EmailStr
from .shared import UserRead, CompanyRead, Roles, UserBase
import re


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=6,
        description="Password with at least 1 uppercase letter, 1 number, and min 6 characters",
    )

    @validator("password")
    def validate_password(cls, v):
        if not re.search(r"^(?=.*[A-Z])(?=.*\d).{6,}$", v):
            raise ValueError(
                "Password must contain at least 1 uppercase letter, 1 number, and be at least 6 characters long"
            )
        return v


class UserResponse(UserRead):
    administered_company: Optional[CompanyRead] = None  # Updated field

    class Config:
        from_attributes = True
        fields = {"refresh_token": {"exclude": True}, "password": {"exclude": True}}


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, title="Name", description="The name of the user")
    email: Optional[EmailStr] = Field(
        None, title="Email", description="The email of the user"
    )
    role: Optional[Roles] = Field(
        None, title="Role", description="The role of the user"
    )
    company_id: Optional[str] = Field(
        None,
        title="Company ID",
        description="The ID of the company associated with the user",
    )
    password: Optional[str] = Field(
        None,
        min_length=6,
        description="Password with at least 1 uppercase letter, 1 number, and min 6 characters",
    )

    @validator("password")
    def validate_password(cls, v):
        if v is not None and not re.search(r"^(?=.*[A-Z])(?=.*\d).{6,}$", v):
            raise ValueError(
                "Password must contain at least 1 uppercase letter, 1 number, and be at least 6 characters long"
            )
        return v
