from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from app.models.profile import ActivityLevel

if TYPE_CHECKING:
    from app.models.user import Users


class StartingPoint(SQLModel, table=True):
    __tablename__ = "starting_points"  # type: ignore[assignment]

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", unique=True, index=True)
    weight_kg: float
    activity_level: ActivityLevel
    training_days_per_week: int
    average_sleep_hours: float | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    user: "Users" = Relationship(back_populates="starting_point")
