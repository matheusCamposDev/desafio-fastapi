import pytest
from sqlmodel import Session, SQLModel, create_engine
from fastapi.testclient import TestClient
from app.main import app
from app.models.client import Client


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)  # Cria as tabelas no banco em memória
    with Session(engine) as session:
        yield session  # retorna uma sessão de teste
