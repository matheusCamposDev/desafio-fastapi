from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from datetime import datetime
from app.models.client import ClientOut
from app.models.orderproduct import OrderProduct, OrderProductOut
from app.models.product import ProductOut


class OrderBase(SQLModel):
    client_id: int = Field(foreign_key="client.id")
    status: str = Field(default="pendente", max_length=50)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


# class OrderProduct(SQLModel, table=True):
#     order_id: int = Field(foreign_key="order.id", primary_key=True)
#     product_id: int = Field(foreign_key="product.id", primary_key=True)
#     quantity: int


class Order(OrderBase, table=True):
    id: int = Field(default=None, primary_key=True)
    client: Optional["Client"] = Relationship(back_populates="orders")
    products: List["Product"] = Relationship(
        back_populates="orders", link_model=OrderProduct
    )
    order_products: List[OrderProduct] = Relationship(
        back_populates="order", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    model_config = {"arbitrary_types_allowed": True}


class OrderProductInput(SQLModel):
    product_id: int
    quantity: int


class OrderCreate(SQLModel):
    client_id: int
    products: List[OrderProductInput]

    class Config:
        orm_mode = True


class OrderUpdate(SQLModel):
    status: Optional[str] = None
    products: Optional[List[OrderProductInput]] = None


class OrderOut(OrderBase):
    id: int
    client: Optional[ClientOut] = None
    order_products: List[OrderProductOut] = []

    class Config:
        orm_mode = True
