from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import CurrentUser, SessionDep
from app.repositories.starting_point import StartingPointRepository
from app.schemas.starting_point import StartingPointCreate, StartingPointRead, StartingPointUpdate
from app.services.starting_point import StartingPointService


router = APIRouter()


def get_starting_point_service(session: SessionDep) -> StartingPointService:
    return StartingPointService(StartingPointRepository(session))


@router.post("/starting-point", response_model=StartingPointRead, status_code=status.HTTP_201_CREATED)
async def create_starting_point(
    data: StartingPointCreate,
    session: SessionDep,
    current_user: CurrentUser,
):
    try:
        return await get_starting_point_service(session).create(current_user.id, data)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/starting-point", response_model=StartingPointRead)
async def get_starting_point(session: SessionDep, current_user: CurrentUser):
    try:
        return await get_starting_point_service(session).get(current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.patch("/starting-point", response_model=StartingPointRead)
async def update_starting_point(
    data: StartingPointUpdate,
    session: SessionDep,
    current_user: CurrentUser,
):
    try:
        return await get_starting_point_service(session).update(current_user.id, data)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
