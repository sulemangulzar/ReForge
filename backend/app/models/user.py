from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class Users(SQLModel, table=True):

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    password_updated_at: datetime = Field(default_factory=datetime.now)
    role: UserRole = UserRole.USER
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
