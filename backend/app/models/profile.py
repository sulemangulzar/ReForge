from datetime import date, datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


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


class Profile(SQLModel, table=True):
    __tablename__ = "profiles"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", unique=True, index=True)
    name: str
    date_of_birth: date
    gender: Gender
    height_cm: float
    current_weight_kg: float
    experience_level: ExperienceLevel
    preferred_units: PreferredUnits
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
