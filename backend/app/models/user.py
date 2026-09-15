from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.goal import Goal
    from app.models.profile import Profile
    from app.models.refresh_token import RefreshToken
    from app.models.starting_point import StartingPoint


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

    profile: "Profile | None" = Relationship(back_populates="user")
    goal: "Goal | None" = Relationship(back_populates="user")
    refresh_tokens: list["RefreshToken"] = Relationship(back_populates="user")
    starting_point: "StartingPoint | None" = Relationship(back_populates="user")
