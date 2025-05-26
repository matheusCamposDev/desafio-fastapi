from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import date


class ProductBase(SQLModel):
    description: str = Field(max_length=255)
    price: float
    barcode: str = Field(max_length=64, unique=True)
    section: str = Field(max_length=100)
    stock: int
    expiry_date: Optional[date] = None
    available: Optional[bool] = True
    image_url: Optional[str] = Field(default=None, max_length=255)


class Product(ProductBase, table=True):
    id: int = Field(default=None, primary_key=True)
    barcode: str = Field(index=True, unique=True)
    section: str = Field(index=True)


class ProductCreate(ProductBase):
    class Config:
        orm_mode = True


class ProductUpdate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
