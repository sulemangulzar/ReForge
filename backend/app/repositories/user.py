from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import Users


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Users | None:
        result = await self.session.exec(select(Users).where(Users.email == email))
        return result.one_or_none()

    async def create(self, user: Users) -> Users:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
