from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jwt import (
    ExpiredSignatureError,
    InvalidSignatureError,
    DecodeError,
    encode,
    decode,
)
from dotenv import load_dotenv
import app.custom_exception as ce
import os


load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    user_id: int,
    expires_delta: timedelta,
    token_type: str,
) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "type": token_type,
    }

    # secret_key = secrets.token_urlsafe(32)

    encoded_jwt = encode(
        to_encode,
        os.getenv("REFRESH_TOKEN_SECRET"),
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def decodify_refresh_token(token: str):
    try:
        payload = decode(
            token,
            os.getenv("REFRESH_TOKEN_SECRET"),
            algorithms=[ALGORITHM],
        )
        user_id = payload["sub"]
        token_type = payload["type"]
        if user_id is None or token_type is None:
            raise Exception("Token sem ID de usuário.")

        return int(user_id)
    except ExpiredSignatureError:
        raise ce.TokenExpired("Refresh token expirado")
    except (InvalidSignatureError, DecodeError):
        raise ce.TokenInvalid("Refresh token inválido")
