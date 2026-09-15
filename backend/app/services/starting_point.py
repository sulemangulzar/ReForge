from uuid import UUID

from app.models.starting_point import StartingPoint
from app.repositories.starting_point import StartingPointRepository
from app.schemas.starting_point import StartingPointCreate, StartingPointUpdate


class StartingPointService:
    def __init__(self, repository: StartingPointRepository):
        self.repository = repository

    async def create(self, user_id: UUID, data: StartingPointCreate) -> StartingPoint:
        if await self.repository.get_by_user_id(user_id):
            raise ValueError("Starting point already exists")
        return await self.repository.create(
            StartingPoint(user_id=user_id, **data.model_dump())
        )

    async def get(self, user_id: UUID) -> StartingPoint:
        starting_point = await self.repository.get_by_user_id(user_id)
        if starting_point is None:
            raise ValueError("Starting point not found")
        return starting_point

    async def update(self, user_id: UUID, data: StartingPointUpdate) -> StartingPoint:
        starting_point = await self.get(user_id)
        values = data.model_dump(exclude_unset=True)
        return await self.repository.update(starting_point, values)
