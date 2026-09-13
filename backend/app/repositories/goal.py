from datetime import datetime
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.goal import Goal


class GoalRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: UUID) -> Goal | None:
        result = await self.session.exec(select(Goal).where(Goal.user_id == user_id))
        return result.one_or_none()

    async def create(self, goal: Goal) -> Goal:
        self.session.add(goal)
        await self.session.commit()
        await self.session.refresh(goal)
        return goal

    async def update(self, goal: Goal, values: dict[str, object]) -> Goal:
        for key, value in values.items():
            setattr(goal, key, value)
        goal.updated_at = datetime.now()
        self.session.add(goal)
        await self.session.commit()
        await self.session.refresh(goal)
        return goal
