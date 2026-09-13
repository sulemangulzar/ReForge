from datetime import date

from pydantic import BaseModel

from app.models.goal import GoalType


class GoalCreate(BaseModel):
    goal_type: GoalType
    target_weight_kg: float
    target_date: date


class GoalUpdate(BaseModel):
    goal_type: GoalType | None = None
    target_weight_kg: float | None = None
    target_date: date | None = None
