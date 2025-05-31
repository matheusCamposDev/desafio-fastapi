import os
from app import security as security_token
from app.models.login_data import LoginData
from app.models.user import User, UserRegister
from app.security import verify_password_hash
from app.security import get_password_hash
from datetime import timedelta
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import select, Session

load_dotenv()


def create_user(session: Session, user: UserRegister) -> User:
    try:
        user_db = User(
            email=user.email,
            full_name=user.full_name,
            is_admin=user.is_admin,
            hashed_password=get_password_hash(user.password),
        )

        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        return user_db

    except IntegrityError as e:
        session.rollback()

        raise HTTPException(
            status_code=400,
            detail="Invalid email. This email is already in use.",
        )


def authenticate(session: Session, loginData: LoginData):
    statement = select(User).where(User.email == loginData.email)
    user = session.exec(statement).first()

    if not user or not verify_password_hash(loginData.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = security_token.create_access_token(
        user.id,
        expires_delta=timedelta(minutes=int(os.getenv("TOKEN_EXPIRES", 15))),
        token_type="access",
    )

    refresh_token = security_token.create_access_token(
        user.id,
        expires_delta=timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRES", 7))),
        token_type="refresh",
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def checkUserByEmail(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user
