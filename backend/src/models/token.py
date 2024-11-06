from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    id: str
    name: str
    email: str
    role: str
    exp: Optional[datetime] = None


class TokenResponse(TokenData):
    token: Optional[str]
