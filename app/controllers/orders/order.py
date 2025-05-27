from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select
from app.models.client import Client
from app.models.product import Product
from app.models.order import Order, OrderCreate, OrderUpdate, OrderOut, OrderProduct
from datetime import datetime
from typing import List, Optional
from app.security import authenticate_user
from sqlmodel import Session
from app.db.session import get_session

router = APIRouter()


@router.get("/orders", response_model=List[OrderOut])
def list_orders(
    session: Session = Depends(get_session),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    section: Optional[str] = None,
    id_pedido: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    cliente: Optional[int] = Query(None),
):
    query = select(Order)
    if start_date and end_date:
        query = query.where(Order.created_at.between(start_date, end_date))
    if id_pedido:
        query = query.where(Order.id == id_pedido)
    if status:
        query = query.where(Order.status == status)
    if cliente:
        query = query.where(Order.client_id == cliente)

    orders = session.exec(query).all()

    # Filtro por seção dos produtos
    if section:
        filtered_orders = []
        for order in orders:
            for product in order.products:
                if product.section == section:
                    filtered_orders.append(order)
                    break
        return filtered_orders

    return orders


@router.post("/orders", response_model=OrderOut, status_code=201)
def create_order(order_data: OrderCreate, session: Session = Depends(get_session)):
    # Verifica se cliente existe
    client = session.get(Client, order_data.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # Cria pedido
    order = Order(client_id=order_data.client_id)
    session.add(order)
    session.flush()  # Garante o ID do pedido

    # Adiciona produtos ao pedido
    for item in order_data.products:
        product = session.get(Product, item.product_id)
        if not product:
            raise HTTPException(
                status_code=404, detail=f"Produto ID {item.product_id} não encontrado"
            )
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Estoque insuficiente para o produto {product.description}",
            )
        product.stock -= item.quantity
        link = OrderProduct(
            order_id=order.id, product_id=product.id, quantity=item.quantity
        )
        session.add(link)

    session.commit()
    session.refresh(order)
    return order


@router.get("/orders/{id}", response_model=OrderOut)
def get_order(id: int, session: Session = Depends(get_session)):
    order = session.get(Order, id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return order


@router.put("/orders/{id}", response_model=OrderOut)
def update_order(
    id: int, update_data: OrderUpdate, session: Session = Depends(get_session)
):
    order = session.get(Order, id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    # Atualiza status
    if update_data.status:
        order.status = update_data.status

    # Atualiza produtos, se fornecido
    if update_data.products is not None:
        # Remove associações antigas
        old_links = session.exec(
            select(OrderProduct).where(OrderProduct.order_id == id)
        ).all()
        for link in old_links:
            session.delete(link)

        # Reprocessa estoque e associações
        for item in update_data.products:
            product = session.get(Product, item.product_id)
            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Produto ID {item.product_id} não encontrado",
                )
            if product.stock < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Estoque insuficiente para o produto {product.description}",
                )
            product.stock -= item.quantity
            link = OrderProduct(
                order_id=id, product_id=product.id, quantity=item.quantity
            )
            session.add(link)

    session.commit()
    session.refresh(order)
    return order


@router.delete("/orders/{id}", status_code=204)
def delete_order(id: int, session: Session = Depends(get_session)):
    order = session.get(Order, id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    session.delete(order)
    session.commit()
    return None
