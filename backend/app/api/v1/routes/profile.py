from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import CurrentUser, SessionDep
from app.repositories.profile import ProfileRepository
from app.schemas.profile import ProfileCreate, ProfileUpdate
from app.services.profile import ProfileService


router = APIRouter()


def get_profile_service(session: SessionDep) -> ProfileService:
    return ProfileService(ProfileRepository(session))


@router.post("/profile", status_code=status.HTTP_201_CREATED)
async def create_profile(data: ProfileCreate, session: SessionDep, current_user: CurrentUser):
    try:
        return await get_profile_service(session).create(current_user.id, data)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/profile")
async def get_profile(session: SessionDep, current_user: CurrentUser):
    try:
        return await get_profile_service(session).get(current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.patch("/profile")
async def update_profile(data: ProfileUpdate, session: SessionDep, current_user: CurrentUser):
    try:
        return await get_profile_service(session).update(current_user.id, data)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
