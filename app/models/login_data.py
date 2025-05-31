from pydantic import BaseModel, EmailStr


class LoginData(BaseModel):
    email: EmailStr
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
