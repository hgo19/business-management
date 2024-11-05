from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, validator
import re

class CompanyBase(BaseModel):
    name: str = Field(..., title="Name", description="The name of the company")
    description: Optional[str] = Field(None, title="Description", description="Description of the company")
    website: Optional[str] = Field(None, title="Website", description="Company website URL")
    contact_email: EmailStr = Field(..., title="Contact Email", description="Primary contact email for the company")
    contact_phone: str = Field(..., title="Contact Phone", description="Primary contact phone number")
    street: Optional[str] = Field(None, title="Street", description="Street address")
    city: Optional[str] = Field(None, title="City", description="City")
    state: Optional[str] = Field(None, title="State", description="State/Province/Region")
    postal_code: str = Field(..., title="Postal Code", description="Postal/ZIP code")
    country: Optional[str] = Field(None, title="Country", description="Country")

    @validator('contact_phone')
    def validate_phone(cls, v):
        if not re.match(r'^\+?[1-9]\d{1,14}$', v):
            raise ValueError("Invalid phone number format")
        return v

class CompanyCreate(CompanyBase):
    pass

class CompanyRead(CompanyBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
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

    @validator('contact_phone')
    def validate_phone(cls, v):
        if v is not None:
            if not re.match(r'^\+?[1-9]\d{1,14}$', v):
                raise ValueError("Invalid phone number format")
        return v

class CompanyResponse(CompanyRead):
    users: Optional[List['UserResponse']] = []

    class Config:
        from_attributes = True

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import UserResponse