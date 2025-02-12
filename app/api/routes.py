from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.client_service import ClientService
from app.repositories.client_repository import ClientRepository
from pydantic import BaseModel

router = APIRouter()

class ClientCreate(BaseModel):
    document: str
    name: str
    is_blocked: bool = False

class ClientOut(BaseModel):
    document: str
    name: str
    is_blocked: bool

    class Config:
        orm_mode = True

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

@router.post("/clientes", response_model=ClientOut)
def create_client(client: ClientCreate, service: ClientService = Depends(get_client_service)):
    try:
        created = service.create_client(document=client.document, name=client.name, is_blocked=client.is_blocked)
        return created
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/clientes", response_model=list[ClientOut])
def list_clients(name: str = None, service: ClientService = Depends(get_client_service)):
    clients = service.get_clients(name)
    return clients

@router.get("/clientes/{document}", response_model=ClientOut)
def get_client(document: str, service: ClientService = Depends(get_client_service)):
    client = service.get_client(document)
    if client is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client
