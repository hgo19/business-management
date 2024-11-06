from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, validator
from enum import Enum

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

class UserRead(UserBase):
    id: str
    refresh_token: Optional[str]
    password: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CompanyBase(BaseModel):
    name: str = Field(..., title="Name", description="The name of the company")
    description: Optional[str] = Field(
        None, title="Description", description="Description of the company"
    )
    website: Optional[str] = Field(
        None, title="Website", description="Company website URL"
    )
    contact_email: EmailStr = Field(
        ..., title="Contact Email", description="Primary contact email for the company"
    )
    contact_phone: str = Field(
        ..., title="Contact Phone", description="Primary contact phone number"
    )
    street: Optional[str] = Field(None, title="Street", description="Street address")
    city: Optional[str] = Field(None, title="City", description="City")
    state: Optional[str] = Field(
        None, title="State", description="State/Province/Region"
    )
    postal_code: str = Field(..., title="Postal Code", description="Postal/ZIP code")
    country: Optional[str] = Field(None, title="Country", description="Country")
    admin_id: str = Field(
        ..., title="Admin ID", description="The ID of the company administrator"
    )

class CompanyRead(CompanyBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
