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
from fastapi import Depends, HTTPException
import app.custom_exception as ce
import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

load_dotenv()
bearer_scheme = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password_hash(plain_password: str, hashed_password: str) -> bool:
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

    encoded_jwt = encode(
        to_encode,
        os.getenv("REFRESH_TOKEN_SECRET"),
        algorithm=os.getenv("ALGORITHM"),
    )
    return encoded_jwt


def decodify_refresh_token(token: str):
    try:
        payload = decode(
            token,
            os.getenv("REFRESH_TOKEN_SECRET"),
            algorithms=[os.getenv("ALGORITHM")],
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


def authenticate_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            os.getenv("REFRESH_TOKEN_SECRET"),
            algorithms=[os.getenv("ALGORITHM")],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
