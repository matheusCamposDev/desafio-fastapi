from fastapi import APIRouter, Response, Depends
from typing import List, Optional
from sqlmodel import Session
from app.db.session import get_session
from app.services import client_service
from app.models.client import ClientOut, ClientCreate, ClientUpdate, Client
from app.security import authenticate_user
from app.response import (
    clients_get_responses,
    clients_create_responses,
    get_client_responses,
    update_client_responses,
    delete_client_responses,
)

router = APIRouter()


@router.get("/clients", response_model=List[ClientOut], responses=clients_get_responses)
def list_clients(
    name: Optional[str] = None,
    email: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session),
) -> Client:
    return client_service.get_clients(db, name, email, skip, limit)


@router.post("/clients", responses=clients_create_responses, status_code=201)
def create_client(
    client: ClientCreate,
    db: Session = Depends(get_session),
) -> Response:
    client_service.verify_client(client, db)

    client_service.create_client(db, client)
    return Response(status_code=201)


@router.get(
    "/clients/{client_id}", response_model=ClientOut, responses=get_client_responses
)
def get_client(client_id: int, db: Session = Depends(get_session)):
    client = client_service.get_client_by_id(client_id, db)
    return client


@router.put(
    "/clients/{client_id}", response_model=ClientOut, responses=update_client_responses
)
def update_client(
    client_id: int,
    updated: ClientUpdate,
    db: Session = Depends(get_session),
):

    client = client_service.update_client(client_id, updated, db)

    return client


@router.delete(
    "/clients/{client_id}", responses=delete_client_responses, status_code=204
)
def delete_client(client_id: int, db: Session = Depends(get_session)) -> Response:
    client_service.delete_client(client_id, db)
    return Response(status_code=204)
