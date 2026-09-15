from uuid import UUID

from sqlmodel import Field, SQLModel

from app.models.profile import ActivityLevel


class StartingPointCreate(SQLModel):
    weight_kg: float = Field(ge=25, le=400)
    activity_level: ActivityLevel
    training_days_per_week: int = Field(ge=0, le=7)
    average_sleep_hours: float | None = Field(default=None, ge=0, le=24)


class StartingPointUpdate(SQLModel):
    weight_kg: float | None = Field(default=None, ge=25, le=400)
    activity_level: ActivityLevel | None = None
    training_days_per_week: int | None = Field(default=None, ge=0, le=7)
    average_sleep_hours: float | None = Field(default=None, ge=0, le=24)


class StartingPointRead(SQLModel):
    id: UUID
    weight_kg: float
    activity_level: ActivityLevel
    training_days_per_week: int
    average_sleep_hours: float | None
