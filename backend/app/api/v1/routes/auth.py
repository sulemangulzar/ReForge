from app.core.dependencies import SessionDep
from fastapi import APIRouter, Cookie, HTTPException, Response

from app.repositories.user import UserRepository
from app.schemas.user import ForgotPassword, ResetPassword, UserLogin, UserRegister
from app.services.user import UserService

router = APIRouter()

@router.post("/register")
async def register(session: SessionDep, data: UserRegister):
    try:
        return await UserService(UserRepository(session)).register(data)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

@router.post("/forgot-password")
async def forgot_password(session: SessionDep, data: ForgotPassword):
    await UserService(UserRepository(session)).forgot_password(data)
    return {"message": "If the email exists, a reset link has been sent"}


@router.post("/reset-password")
async def reset_password(session: SessionDep, data: ResetPassword):
    try:
        await UserService(UserRepository(session)).reset_password(data)
        return {"message": "Password reset successfully"}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/login")
async def login(response: Response, session: SessionDep, data: UserLogin):
    try:
        _, access_token, refresh_token = await UserService(UserRepository(session)).login(data)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=7 * 24 * 60 * 60,
            path="/auth",
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc


@router.post("/refresh")
async def refresh(session: SessionDep, refresh_token: str | None = Cookie(default=None)):
    if refresh_token is None:
        raise HTTPException(status_code=401, detail="Refresh token is missing")
    try:
        access_token = await UserService(UserRepository(session)).refresh(refresh_token)
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc


@router.post("/signout")
async def signout(response: Response, session: SessionDep, refresh_token: str | None = Cookie(default=None)):
    if refresh_token is not None:
        try:
            await UserService(UserRepository(session)).signout(refresh_token)
        except ValueError as exc:
            raise HTTPException(status_code=401, detail=str(exc)) from exc
    response.delete_cookie(key="refresh_token", path="/auth")
    return {"message": "Signed out"}


@router.get("/confirm-email")
async def confirm_email(token: str, session: SessionDep):
    try:
        await UserService(UserRepository(session)).confirm_email(token)
        return {"message": "Email confirmed"}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

