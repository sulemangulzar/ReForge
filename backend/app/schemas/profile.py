from datetime import date

from pydantic import BaseModel

from app.models.profile import (
    ActivityLevel,
    ExperienceLevel,
    Gender,
    PreferredUnits,
    TrainingFrequency,
)


class ProfileCreate(BaseModel):
    name: str
    date_of_birth: date
    gender: Gender
    height_cm: float
    current_weight_kg: float
    activity_level: ActivityLevel
    training_frequency: TrainingFrequency
    experience_level: ExperienceLevel
    preferred_units: PreferredUnits


class ProfileUpdate(BaseModel):
    name: str | None = None
    date_of_birth: date | None = None
    gender: Gender | None = None
    height_cm: float | None = None
    current_weight_kg: float | None = None
    activity_level: ActivityLevel | None = None
    training_frequency: TrainingFrequency | None = None
    experience_level: ExperienceLevel | None = None
    preferred_units: PreferredUnits | None = None
