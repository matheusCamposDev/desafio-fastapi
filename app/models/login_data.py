from pydantic import BaseModel


class LoginData(BaseModel):
    email: str
    username: str
    password: str
