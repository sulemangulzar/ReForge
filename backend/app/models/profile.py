from datetime import date, datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import Users


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class ExperienceLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class PreferredUnits(str, Enum):
    METRIC = "metric"
    IMPERIAL = "imperial"


class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    ACTIVE = "active"
    VERY_ACTIVE = "very_active"


class TrainingFrequency(str, Enum):
    ZERO_DAYS = "0 days"
    ONE_TWO_DAYS = "1–2 days"
    THREE_FOUR_DAYS = "3–4 days"
    FIVE_PLUS_DAYS = "5+ days"


class Profile(SQLModel, table=True):
    __tablename__ = "profiles"  # type: ignore[assignment]

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", unique=True, index=True)
    name: str
    date_of_birth: date
    gender: Gender
    height_cm: float
    current_weight_kg: float
    activity_level: ActivityLevel
    training_frequency: TrainingFrequency
    experience_level: ExperienceLevel
    preferred_units: PreferredUnits
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    user: "Users" = Relationship(back_populates="profile")
