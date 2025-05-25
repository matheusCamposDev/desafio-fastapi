from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import jwt
import os

load_dotenv()
client = TestClient(app)


def create_test_token(user_id: int, exp_delta: timedelta, type: str):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + exp_delta,
        "type": type,
    }
    return jwt.encode(
        payload,
        os.getenv("REFRESH_TOKEN_SECRET"),
        algorithm=os.getenv("ALGORITHM"),
    )


def test_refresh_success(client):
    token = create_test_token(1, timedelta(minutes=5), "refresh")

    response = client.post("/auth/refresh", json={"refresh_token": token})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_refresh_expired_token(client):
    token = create_test_token(1, timedelta(minutes=-5), "refresh")  # token já expirado

    response = client.post("/auth/refresh", json={"refresh_token": token})
    assert response.status_code == 401
    assert response.json()["detail"] == "Refresh token expirado"


def test_refresh_invalid_signature(client):
    # Token com assinatura errada
    payload = {
        "sub": "1",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
        "type": "refresh",
    }
    token = jwt.encode(payload, "wrong_secret", algorithm=os.getenv("ALGORITHM"))

    response = client.post("/auth/refresh", json={"refresh_token": token})
    assert response.status_code == 401
    assert response.json()["detail"] == "Refresh token inválido"


def test_refresh_malformed_token(client):
    token = "isso_nao_e_um_token"

    response = client.post("/auth/refresh", json={"refresh_token": token})
    assert response.status_code == 401
    assert response.json()["detail"] == "Refresh token inválido"
