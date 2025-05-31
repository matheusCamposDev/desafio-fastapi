import app.custom_exception as ce
import os
from app.models.login_data import LoginData, LoginResponse
from app.models.refresh_token import TokenRefreshRequest
from app.models.user import UserRegister, UserRead
from app import security as security_token
from app.services import auth_service
from app.db.session import get_session
from app.response import register_responses, login_responses, refresh_token_reponses
from datetime import timedelta
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Any
from sqlmodel import Session

load_dotenv()

router = APIRouter()


@router.post("/register", response_model=UserRead, responses=register_responses)
def register(user_in: UserRegister, session: Session = Depends(get_session)):
    """
    Create a new user.
    """
    auth_service.create_user(session=session, user=user_in)

    return JSONResponse(
        status_code=201, content={"detail": "User created successfully"}
    )


@router.post("/login", response_model=LoginResponse, responses=login_responses)
def login_access_token(form_data: LoginData, session: Session = Depends(get_session)):
    """
    Login with access token.
    """
    token = auth_service.authenticate(session=session, loginData=form_data)

    return JSONResponse(
        status_code=200,
        content={
            "access_token": token["access_token"],
            "refresh_token": token["refresh_token"],
            "token_type": token["token_type"],
        },
    )


@router.post("/refresh", responses={**refresh_token_reponses})
def refresh_token(request: TokenRefreshRequest) -> Any:

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
