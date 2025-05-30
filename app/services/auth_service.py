from sqlalchemy.exc import IntegrityError
from app.models.user import User, UserRegister
from app.security import verify_password
from sqlmodel import select, Session
from fastapi import HTTPException
from app.security import get_password_hash


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


def authenticate(session: Session, email: str, password: str) -> User | None:
    db_user = checkUserByEmail(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def checkUserByEmail(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user
