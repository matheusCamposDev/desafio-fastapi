from sqlmodel import Field, SQLModel
from pydantic import EmailStr


class ClientBase(SQLModel):
    name: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
    cpf: str = Field(max_length=11, min_length=11, regex=r"^\d{11}$")


class Client(ClientBase, table=True):
    id: int = Field(primary_key=True)
    email: str = Field(index=True, unique=True)
    cpf: str = Field(index=True, unique=True)


class ClientCreate(ClientBase):
    class Config:
        orm_mode = True


class ClientUpdate(ClientBase):
    pass


class ClientOut(ClientBase):
    id: int

    class Config:
        orm_mode = True
