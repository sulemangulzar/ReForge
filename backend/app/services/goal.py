from uuid import UUID

from app.models.goal import Goal
from app.repositories.goal import GoalRepository
from app.schemas.goal import GoalCreate, GoalUpdate


class GoalService:
    def __init__(self, repository: GoalRepository):
        self.repository = repository

    async def create(self, user_id: UUID, data: GoalCreate) -> Goal:
        if await self.repository.get_by_user_id(user_id):
            raise ValueError("Current goal already exists")
        return await self.repository.create(Goal(user_id=user_id, **data.model_dump()))

    async def get_current(self, user_id: UUID) -> Goal:
        goal = await self.repository.get_by_user_id(user_id)
        if goal is None:
            raise ValueError("Current goal not found")
        return goal

    async def update(self, user_id: UUID, data: GoalUpdate) -> Goal:
        goal = await self.get_current(user_id)
        values = {key: value for key, value in data.model_dump(exclude_unset=True).items() if value is not None}
        return await self.repository.update(goal, values)
