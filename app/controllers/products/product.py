from fastapi import APIRouter, Response, Depends, status
from typing import List, Optional
from sqlmodel import Session
from app.db.session import get_session
from app.models.product import Product, ProductCreate, ProductUpdate, ProductOut
from fastapi import HTTPException
from app.security import authenticate_user
from app.services import product_service
from app.response import (
    products_list_responses,
    product_create_responses,
    product_by_id_responses,
    product_put_responses,
    product_delete_responses,
)

router = APIRouter(dependencies=[Depends(authenticate_user)])


@router.get(
    "/products",
    response_model=List[ProductOut],
    responses=products_list_responses,
)
def list_products(
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    available: Optional[bool] = None,
):
    return product_service.get_products(
        db,
        skip,
        limit,
        category,
        min_price,
        max_price,
        available,
    )


@router.post(
    "/products",
    response_model=ProductOut,
    responses=product_create_responses,
    status_code=201,
)
def create_product(product: ProductCreate, db: Session = Depends(get_session)):
    return product_service.create_product(product, db)


@router.get(
    "/products/{id}",
    response_model=ProductOut,
    responses=product_by_id_responses,
)
def get_product(id: int, db: Session = Depends(get_session)):
    return product_service.get_product_by_id(id, db)


@router.put(
    "/products/{id}",
    response_model=ProductOut,
    responses=product_put_responses,
)
def update_product(
    id: int, product_data: ProductUpdate, db: Session = Depends(get_session)
):
    return product_service.put_product(id, product_data, db)


@router.delete(
    "/products/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=product_delete_responses,
)
def delete_product(id: int, db: Session = Depends(get_session)):
    return product_service.delete_product(id, db)
