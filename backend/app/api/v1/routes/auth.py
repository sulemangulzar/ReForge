from app.core.dependencies import SessionDep
from fastapi import APIRouter, HTTPException

from app.repositories.user import UserRepository
from app.schemas.user import UserRegister
from app.services.user import UserService

router = APIRouter()

@router.post("/register")
async def register(session: SessionDep, data: UserRegister):
    try:
        return await UserService(UserRepository(session)).register(data)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

@router.post("/login")
async def login():
    pass
