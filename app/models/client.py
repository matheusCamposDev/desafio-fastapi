from sqlmodel import Field, Relationship, SQLModel
from pydantic import EmailStr
from typing import List


class ClientBase(SQLModel):
    name: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
    cpf: str = Field(max_length=11, min_length=11, regex=r"^\d{11}$")


class Client(ClientBase, table=True):
    id: int = Field(primary_key=True)
    email: str = Field(index=True, unique=True)
    cpf: str = Field(index=True, unique=True)
    orders: List["Order"] = Relationship(back_populates="client")


class ClientCreate(ClientBase):
    class Config:
        orm_mode = True


class ClientUpdate(ClientBase):
    pass


class ClientOut(ClientBase):
    id: int

    class Config:
        orm_mode = True
