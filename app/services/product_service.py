from app.models.product import Product, ProductUpdate
from sqlmodel import select, Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


def get_products(
    session: Session,
    skip: int = 0,
    limit: int = 0,
    category: str = None,
    min_price: float = None,
    max_price: float = None,
    available: bool = None,
):
    query = select(Product)

    if category:
        query = query.filter(Product.section == category)
    if min_price:
        query = query.filter(Product.price >= min_price)
    if max_price:
        query = query.filter(Product.price <= max_price)
    if available is not None:
        query = query.filter(Product.available == available)

    products = session.exec(query.offset(skip).limit(limit)).all()

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No products found with the given criteria.",
        )
    return products


def create_product(product: Product, db: Session) -> Product:
    try:
        db_product = Product(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except IntegrityError as e:
        db.rollback()
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A product with this barcode already exists.",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating product",
        )


def get_product_by_id(id: int, db: Session) -> Product:
    statement = select(Product).where(Product.id == id)
    product = db.exec(statement).first()

    if not product:
        raise HTTPException(status_code=404, detail=f"Product {id} not found.")
    return product


def put_product(id: int, product_data: ProductUpdate, db: Session) -> Product:
    try:
        statement = select(Product).where(Product.id == id)
        product = db.exec(statement).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        for key, value in product_data.model_dump().items():
            setattr(product, key, value)

        db.commit()
        db.refresh(product)
        return product
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error updating product",
        )


def delete_product(id: int, db: Session) -> None:
    statement = select(Product).where(Product.id == id)
    product = db.exec(statement).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found."
        )

    try:
        db.delete(product)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product {id} cannot be deleted due to existing references.",
        )
