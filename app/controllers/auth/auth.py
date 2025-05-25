from fastapi import APIRouter, HTTPException, Depends
from typing import Any
from app.models.login_data import LoginData
from app.models.refresh_token import TokenRefreshRequest
from app.models.user import UserRegister, UserCreate
from app.services import user_service
from sqlmodel import Session
from app.db.session import get_session
from app.response import register_responses, login_responses, refresh_token_reponses
from fastapi.responses import JSONResponse
from datetime import timedelta
from dotenv import load_dotenv
from app import security as security_token
import app.custom_exception as ce
import os

load_dotenv()

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


@router.post("/login", responses={**login_responses})
def login_access_token(form_data: LoginData, session: Session = Depends(get_session)):
    """
    Login with acess token,
    """
    user = user_service.authenticate(
        session=session,
        email=form_data.email,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=int(os.getenv("TOKEN_EXPIRES")))
    refresh_token_expires = timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRES")))

    access_token = security_token.create_access_token(
        user.id,
        expires_delta=access_token_expires,
        token_type="access",
    )

    refresh_token = security_token.create_access_token(
        user.id,
        expires_delta=refresh_token_expires,
        token_type="refresh",
    )

    return JSONResponse(
        content={
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
        status_code=200,
    )


@router.post("/refresh", responses={**refresh_token_reponses})
def refresh_token(request: TokenRefreshRequest):

    try:
        user_id = security_token.decodify_refresh_token(request.refresh_token)
        access_token_expires = timedelta(minutes=int(os.getenv("TOKEN_EXPIRES")))
        access_token = security_token.create_access_token(
            user_id,
            access_token_expires,
            token_type="access",
        )

        return JSONResponse(
            content={"access_token": access_token},
            status_code=200,
        )

    except ce.TokenExpired as e:
        raise HTTPException(status_code=401, detail=str(e))
    except ce.TokenInvalid as e:
        raise HTTPException(status_code=401, detail=str(e))
