from fastapi import APIRouter, HTTPException, Depends
from typing import Any
from app.models.user import UserRegister, UserCreate
from app.services import user_service
from sqlmodel import Session
from app.db.session import get_session
from app.response import register_responses
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/register", responses={**register_responses})
def register(user_in: UserRegister, session: Session = Depends(get_session)) -> Any:
    """
    Create new user.
    """
    user = user_service.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user_create = UserCreate.model_validate(user_in)
    user_service.create_user(session=session, user_create=user_create)
    return JSONResponse({"Created": "User Created!"}, status_code=201)
