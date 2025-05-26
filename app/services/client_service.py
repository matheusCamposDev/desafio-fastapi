from sqlmodel import select, Session
from app.models.client import Client, ClientCreate
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError


def get_clients(
    session: Session, name: str, email: str, skip: int, limit: int
) -> list[Client]:

    query = select(Client)

    if name:
        query = query.where(Client.name.contains(name))
    if email:
        query = query.where(Client.email.contains(email))

    result = session.exec(query.offset(skip).limit(limit))
    clients = result.all()
    if not clients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No clients found with the given criteria.",
        )

    return clients


def create_client(session: Session, client_data: Client) -> Client:
    try:
        client_obj = Client(**client_data.model_dump())
        session.add(client_obj)
        session.commit()
        session.refresh(client_obj)
        return client_obj
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ou CPF já cadastrado.",
        )


def verify_client(client: Client, db: Session) -> None:
    statement = select(Client).where(
        (Client.email == client.email) | (Client.cpf == client.cpf)
    )
    result = db.exec(statement).first()

    if result:
        if result.email == client.email or result.cpf == client.cpf:
            raise HTTPException(status_code=400, detail="Email ou CPF já cadastrado")


def get_client_by_id(client_id: int, db: Session) -> Client:
    statement = select(Client).where(Client.id == client_id)

    client = db.exec(statement).first()

    if not client:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente ID {client_id} não encontrado",
        )
    return client


def update_client(client_id: int, updated: ClientCreate, db: Session) -> Client:
    try:
        statement = select(Client).where(Client.id == client_id)
        client = db.exec(statement).first()

        if not client:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        # Verificar email único
        email_not_unique = db.exec(
            select(Client).where(
                (Client.email == updated.email) & (Client.id != client_id)
            )
        ).first()
        if email_not_unique:
            raise HTTPException(status_code=400, detail="Insira um email válido.")

        # Verificar cpf único
        cpf_not_unique = db.exec(
            select(Client).where((Client.cpf == updated.cpf) & (Client.id != client_id))
        ).first()
        if cpf_not_unique:
            raise HTTPException(status_code=400, detail="Insira um CPF válido.")

        for key, value in updated.model_dump().items():
            setattr(client, key, value)
        db.commit()
        db.refresh(client)
        return client
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao atualizar cliente. Verifique os dados.",
        )


def delete_client(client_id: int, db: Session) -> None:
    try:
        statement = select(Client).where(Client.id == client_id)
        client = db.exec(statement).first()

        if not client:
            raise HTTPException(
                status_code=404,
                detail=f"Cliente {client_id} não encontrado",
            )

        db.delete(client)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao deletar cliente. Verifique os dados.",
        )
