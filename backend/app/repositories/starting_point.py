from datetime import datetime
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.starting_point import StartingPoint


class StartingPointRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: UUID) -> StartingPoint | None:
        result = await self.session.exec(
            select(StartingPoint).where(StartingPoint.user_id == user_id)
        )
        return result.one_or_none()

    async def create(self, starting_point: StartingPoint) -> StartingPoint:
        self.session.add(starting_point)
        await self.session.commit()
        await self.session.refresh(starting_point)
        return starting_point

    async def update(self, starting_point: StartingPoint, values: dict[str, object]) -> StartingPoint:
        for key, value in values.items():
            setattr(starting_point, key, value)
        starting_point.updated_at = datetime.now()
        self.session.add(starting_point)
        await self.session.commit()
        await self.session.refresh(starting_point)
        return starting_point
