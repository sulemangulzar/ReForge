from app.core.security import hash_password
from app.models.user import Users
from app.repositories.user import UserRepository
from app.schemas.user import UserRegister


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register(self, data: UserRegister) -> Users:
        if await self.repository.get_by_email(data.email):
            raise ValueError("Email already registered")

        user = Users(
            name=data.name,
            email=data.email,
            password_hash=hash_password(data.password),
        )
        return await self.repository.create(user)
