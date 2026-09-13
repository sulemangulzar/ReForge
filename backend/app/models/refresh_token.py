from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    token_hash: str = Field(unique=True, index=True)
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.now)
