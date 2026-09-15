from datetime import date, datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import Users


class GoalType(str, Enum):
    LOSE_FAT = "lose_fat"
    GAIN_MUSCLE = "gain_muscle"
    RECOMPOSITION = "recomposition"
    MAINTAIN = "maintain"
    GAIN_STRENGTH = "gain_strength"


class Goal(SQLModel, table=True):
    __tablename__ = "goals"  # type: ignore[assignment]

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", unique=True, index=True)
    goal_type: GoalType
    target_weight_kg: float
    target_date: date
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    user: "Users" = Relationship(back_populates="goal")
