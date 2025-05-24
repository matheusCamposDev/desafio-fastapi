from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.models.user import User

client = TestClient(app)


def test_login_status_code_200() -> None:
    with patch("app.services.user_service.authenticate") as mock_auth:
        # retornar um usuário válido qualquer
        mock_auth.return_value = User(
            id=1,
            name="str",
            email="str",
        )

        # dados do payload para fazer o client.post funcionar
        payload = {
            "email": "str",
            "username": "str",
            "password": "str",
        }

        response = client.post("/auth/login", json=payload)
        data = response.json()

        assert response.status_code == 200
        assert "refresh_token" and "access_token" in data
