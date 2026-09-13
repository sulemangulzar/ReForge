from datetime import datetime

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from app.models.refresh_token import RefreshToken
from app.models.user import Users


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Users | None:
        result = await self.session.exec(select(Users).where(Users.email == email))
        return result.one_or_none()

    async def get_by_id(self, user_id: UUID) -> Users | None:
        return await self.session.get(Users, user_id)

    async def create(self, user: Users) -> Users:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def verify(self, user: Users) -> Users:
        user.is_verified = True
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_password(self, user: Users, password_hash: str) -> Users:
        user.password_hash = password_hash
        user.password_updated_at = datetime.now()
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def create_refresh_token(self, token: RefreshToken) -> RefreshToken:
        self.session.add(token)
        await self.session.commit()
        await self.session.refresh(token)
        return token

    async def get_refresh_token(self, token_hash: str) -> RefreshToken | None:
        result = await self.session.exec(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )
        return result.one_or_none()

    async def delete_refresh_tokens(self, user_id: UUID) -> None:
        result = await self.session.exec(
            select(RefreshToken).where(RefreshToken.user_id == user_id)
        )
        for token in result.all():
            await self.session.delete(token)
        await self.session.commit()
