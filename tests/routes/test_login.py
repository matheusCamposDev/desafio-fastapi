from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.models.login_data import LoginData
from app.models.user import User

client = TestClient(app)


def test_login_status_code_200() -> None:
    # ARRANGE
    with patch("app.services.auth_service.authenticate") as mock_auth:
        mock_auth.return_value = {
            "access_token": "valid_access_token",
            "refresh_token": "valid_refresh_token",
            "token_type": "bearer",
        }

        payload = {
            "email": "user@teste.com",
            "username": "str",
            "password": "senha@teste",
        }

        # ACT
        response = client.post("/auth/login", json=payload)
        data = response.json()

        # ASSERT
        assert response.status_code == 200
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
