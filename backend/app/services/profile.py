from uuid import UUID

from app.models.profile import Profile
from app.repositories.profile import ProfileRepository
from app.schemas.profile import ProfileCreate, ProfileUpdate


class ProfileService:
    def __init__(self, repository: ProfileRepository):
        self.repository = repository

    async def create(self, user_id: UUID, data: ProfileCreate) -> Profile:
        if await self.repository.get_by_user_id(user_id):
            raise ValueError("Profile already exists")
        return await self.repository.create(Profile(user_id=user_id, **data.model_dump()))

    async def get(self, user_id: UUID) -> Profile:
        profile = await self.repository.get_by_user_id(user_id)
        if profile is None:
            raise ValueError("Profile not found")
        return profile

    async def update(self, user_id: UUID, data: ProfileUpdate) -> Profile:
        profile = await self.get(user_id)
        values = {key: value for key, value in data.model_dump(exclude_unset=True).items() if value is not None}
        return await self.repository.update(profile, values)
