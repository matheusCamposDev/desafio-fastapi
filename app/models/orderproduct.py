from sqlmodel import Relationship, SQLModel, Field
from pydantic import BaseModel


class OrderProduct(SQLModel, table=True):
    order_id: int = Field(foreign_key="order.id", primary_key=True)
    product_id: int = Field(foreign_key="product.id", primary_key=True)
    quantity: int
    order: "Order" = Relationship(back_populates="order_products")
    product: "Product" = Relationship()


class OrderProductOut(BaseModel):
    order_id: int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True
