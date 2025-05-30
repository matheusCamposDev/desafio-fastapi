from sqlmodel import Session
from app.services import user_service
from app.models.user import UserRegister
from ..utils import random_email, random_lower_string, random_bool


def test_create_user(db: Session) -> None:
    email = random_email()  # Gera um email aleatório
    password = random_lower_string()  # Gera um password aleatório
    full_name = random_lower_string()  # gera um full name aleatório
    is_admin = random_bool()  # gera um True ou False aleatório
    user_in = UserRegister(
        email=email,
        is_admin=is_admin,
        full_name=full_name,
        password=password,
    )
    user = user_service.create_user(session=db, user_create=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")
