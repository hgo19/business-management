from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, EmailStr, validator
from enum import Enum
import re


class Roles(str, Enum):
    admin = "admin"
    superadmin = "superadmin"
    operator = "operator"


class UserBase(BaseModel):
    name: str = Field(..., title="Name", description="The name of the user")
    email: EmailStr = Field(..., title="Email", description="The email of the user")
    role: Roles = Field(..., title="Role", description="The role of the user")
    company_id: Optional[str] = Field(
        None,
        title="Company ID",
        description="The ID of the company associated with the user",
    )


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


class UserRead(UserCreate):
    id: str
    refresh_token: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(UserBase):
    password: Optional[str] = Field(
        None,
        min_length=6,
        description="Password with at least 1 uppercase letter, 1 number, and min 6 characters",
    )

    @validator("password", always=True)
    def validate_password(cls, v):
        if v is not None and not re.search(r"^(?=.*[A-Z])(?=.*\d).{6,}$", v):
            raise ValueError(
                "Password must contain at least 1 uppercase letter, 1 number, and be at least 6 characters long"
            )
        return v


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(UserRead):
    administered_companies: Optional[List[Dict]] = []

    class Config:
        from_attributes = True
        fields = {"refresh_token": {"exclude": True}, "password": {"exclude": True}}
