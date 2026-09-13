from datetime import datetime
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.profile import Profile


class ProfileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: UUID) -> Profile | None:
        result = await self.session.exec(select(Profile).where(Profile.user_id == user_id))
        return result.one_or_none()

    async def create(self, profile: Profile) -> Profile:
        self.session.add(profile)
        await self.session.commit()
        await self.session.refresh(profile)
        return profile

    async def update(self, profile: Profile, values: dict[str, object]) -> Profile:
        for key, value in values.items():
            setattr(profile, key, value)
        profile.updated_at = datetime.now()
        self.session.add(profile)
        await self.session.commit()
        await self.session.refresh(profile)
        return profile
