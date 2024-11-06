from typing import Optional, List
from pydantic import BaseModel, EmailStr, validator
from .shared import UserRead, CompanyRead
import re


class CompanyCreate(CompanyRead):
    pass


class CompanyResponse(CompanyRead):
    users: Optional[List[UserRead]] = []
    admin: Optional[UserRead] = None

    class Config:
        from_attributes = True


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    admin_id: Optional[str] = None

    @validator("contact_phone")
    def validate_phone(cls, v):
        if v is not None and not re.match(r"^\+?[1-9]\d{1,14}$", v):
            raise ValueError("Invalid phone number format")
        return v
