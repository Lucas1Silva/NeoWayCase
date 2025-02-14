from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import SessionLocal
from app.repositories.client_repository import ClientRepository
from app.services.client_service import ClientService
from app.dependencies import get_current_user  #

router = APIRouter()

# Esquemas Pydantic
class ClientCreate(BaseModel):
    document: str
    name: str
    is_blocked: bool = False

class ClientOut(BaseModel):
    document: str
    name: str
    is_blocked: bool

    class Config:
        # No Pydantic V2, 'orm_mode' foi renomeado para 'from_attributes'
        from_attributes = True

# Dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_client_service(db: Session = Depends(get_db)):
    repo = ClientRepository(db)
    return ClientService(repo)

@router.post("/", response_model=ClientOut)
def create_client(
    client: ClientCreate,
    service: ClientService = Depends(get_client_service),
    current_user: str = Security(get_current_user)  # Usa Security da dependência correta
):
    try:
        created = service.create_client(
            document=client.document,
            name=client.name,
            is_blocked=client.is_blocked
        )
        return created
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ClientOut])
def list_clients(
    name: str = None,
    service: ClientService = Depends(get_client_service),
    current_user: str = Security(get_current_user)
):
    clients = service.get_clients(name)
    return clients

@router.get("/{document}", response_model=ClientOut)
def get_client(
    document: str,
    service: ClientService = Depends(get_client_service),
    current_user: str = Security(get_current_user)
):
    client = service.get_client(document)
    if client is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client
