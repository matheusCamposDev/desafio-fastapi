from fastapi import status, HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.models.client import Client
from app.main import app
from app.db.session import get_session  # onde está o get_session real

client = TestClient(app)


mock_data = [
    Client(id=1, name="João", email="joao@email.com", cpf="12345678901"),
    Client(id=2, name="Maria", email="maria@email.com", cpf="10987654321"),
]


@patch("app.services.client_service.get_clients")
def test_list_clients_success(mock_get_clients, client):
    mock_get_clients.return_value = mock_data
    response = client.get("/clients?skip=0&limit=10")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "João"
    assert data[1]["email"] == "maria@email.com"


@patch("app.services.client_service.get_clients")
def test_list_clients_filter_by_name(mock_get_clients, client):
    mock_get_clients.return_value = [
        Client(id=2, name="Maria", email="maria@email.com")
    ]

    response = client.get("/clients?name=Maria&skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Maria"


@patch("app.services.client_service.update_client")
def test_update_client_success(mock_update_client, client):
    updated_data = {
        "name": "Novo Nome",
        "email": "novo@email.com",
        "cpf": "12345678900",
    }
    client_id = 1

    mock_update_client.return_value = Client(id=client_id, **updated_data)

    response = client.put(f"/clients/{client_id}", json=updated_data)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Novo Nome"
    assert data["email"] == "novo@email.com"
