from pydantic import BaseModel


class UserRegister(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class ForgotPassword(BaseModel):
    email: str


class ResetPassword(BaseModel):
    token: str
    password: str
