from datetime import datetime, timedelta
from uuid import UUID

from app.core.security import (
    create_email_confirmation_token,
    create_password_reset_token,
    create_refresh_token,
    create_token,
    hash_password,
    hash_token,
    verify_email_confirmation_token,
    verify_password,
    verify_password_reset_token,
    verify_refresh_token,
)
from app.services.email_confirm import send_confirmation_email, send_password_reset_email
from app.models.refresh_token import RefreshToken
from app.models.user import Users
from app.repositories.user import UserRepository
from app.schemas.user import ForgotPassword, ResetPassword, UserLogin, UserRegister


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register(self, data: UserRegister) -> Users:
        if await self.repository.get_by_email(data.email):
            raise ValueError("Email already registered")

        user = Users(
            email=data.email,
            password_hash=hash_password(data.password),
        )
        user = await self.repository.create(user)
        token = create_email_confirmation_token(user.email)
        send_confirmation_email(user.email, token)
        return user

    async def forgot_password(self, data: ForgotPassword) -> None:
        user = await self.repository.get_by_email(data.email)
        if user is not None:
            token = create_password_reset_token(user.email)
            send_password_reset_email(user.email, token)

    async def reset_password(self, data: ResetPassword) -> None:
        email = verify_password_reset_token(data.token)
        user = await self.repository.get_by_email(email)
        if user is None:
            raise ValueError("User not found")
        await self.repository.update_password(user, hash_password(data.password))
        await self.repository.delete_refresh_tokens(user.id)

    async def login(self, data: UserLogin) -> tuple[Users, str, str]:
        user = await self.repository.get_by_email(data.email)
        if user is None or not verify_password(data.password, user.password_hash):
            raise ValueError("Invalid email or password")
        if not user.is_verified:
            raise ValueError("Email is not verified")
        if not user.is_active:
            raise ValueError("User is inactive")

        claims = {
            "sub": str(user.id),
            "role": user.role.value,
            "is_verified": user.is_verified,
        }
        access_token = create_token(claims)
        refresh_token = create_refresh_token(claims)
        await self.repository.create_refresh_token(
            RefreshToken(
                user_id=user.id,
                token_hash=hash_token(refresh_token),
                expires_at=datetime.now() + timedelta(days=7),
            )
        )
        return user, access_token, refresh_token

    async def signout(self, token: str) -> None:
        payload = verify_refresh_token(token)
        await self.repository.delete_refresh_tokens(UUID(payload["sub"]))

    async def refresh(self, token: str) -> str:
        payload = verify_refresh_token(token)
        stored_token = await self.repository.get_refresh_token(hash_token(token))
        if stored_token is None or stored_token.expires_at <= datetime.now():
            raise ValueError("Invalid refresh token")
        return create_token(
            {
                "sub": payload["sub"],
                "role": payload["role"],
                "is_verified": payload["is_verified"],
            }
        )

    async def confirm_email(self, token: str) -> Users:
        email = verify_email_confirmation_token(token)
        user = await self.repository.get_by_email(email)
        if user is None:
            raise ValueError("User not found")
        return await self.repository.verify(user)
