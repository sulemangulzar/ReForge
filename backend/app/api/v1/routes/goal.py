from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import CurrentUser, SessionDep
from app.repositories.goal import GoalRepository
from app.schemas.goal import GoalCreate, GoalUpdate
from app.services.goal import GoalService


router = APIRouter()


def get_goal_service(session: SessionDep) -> GoalService:
    return GoalService(GoalRepository(session))


@router.post("/goals", status_code=status.HTTP_201_CREATED)
async def create_goal(data: GoalCreate, session: SessionDep, current_user: CurrentUser):
    try:
        return await get_goal_service(session).create(current_user.id, data)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/goals/current")
async def get_current_goal(session: SessionDep, current_user: CurrentUser):
    try:
        return await get_goal_service(session).get_current(current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.patch("/goals/current")
async def update_current_goal(data: GoalUpdate, session: SessionDep, current_user: CurrentUser):
    try:
        return await get_goal_service(session).update(current_user.id, data)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
