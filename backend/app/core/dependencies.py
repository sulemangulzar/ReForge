from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.core.security import verify_token
from app.models.user import UserRole, Users
from app.repositories.user import UserRepository


SessionDep = Annotated[AsyncSession, Depends(get_session)]

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    session: SessionDep,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> Users:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = verify_token(credentials.credentials)
        user_id = UUID(payload["sub"])
    except (ValueError, KeyError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await UserRepository(session).get_by_id(user_id)
    if user is None or not user.is_active or not user.is_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
    return user


CurrentUser = Annotated[Users, Depends(get_current_user)]


def require_role(role: UserRole):
    async def role_checker(current_user: CurrentUser) -> Users:
        if current_user.role != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user

    return role_checker
