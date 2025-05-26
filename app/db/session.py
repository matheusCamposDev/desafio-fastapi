from sqlmodel import Session, SQLModel, create_engine
import os
from dotenv import load_dotenv
from app.models.user import User
from app.models.client import Client
from app.models.product import Product

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
