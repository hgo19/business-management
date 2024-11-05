from sqlalchemy.orm import DeclarativeBase
import enum
from datetime import datetime
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.sql import func
import uuid
from typing import List, Optional


class Base(DeclarativeBase):
    pass


class Roles(enum.Enum):
    admin = "admin"
    superadmin = "super_admin"
    operator = "operator"


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    website: Mapped[Optional[str]] = mapped_column(nullable=True)
    contact_email: Mapped[str] = mapped_column(nullable=False)
    contact_phone: Mapped[str] = mapped_column(nullable=False)
    street: Mapped[Optional[str]] = mapped_column(nullable=True)
    city: Mapped[Optional[str]] = mapped_column(nullable=True)
    state: Mapped[Optional[str]] = mapped_column(nullable=True)
    postal_code: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    users: Mapped[List["User"]] = relationship(back_populates="company")

    def __repr__(self) -> str:
        return f"Company(id={self.id!r}, name={self.name!r})"


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[Roles] = mapped_column(Enum(Roles), nullable=False)
    refresh_token: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    company_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("companies.id"), nullable=True
    )
    company: Mapped[Optional["Company"]] = relationship(back_populates="users")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"
