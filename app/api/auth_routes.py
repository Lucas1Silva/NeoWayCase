from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import SessionLocal
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

router = APIRouter()

# Schemas para registro e login
class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_auth_service(db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    return AuthService(user_repo)

@router.post("/register", response_model=Token)
def register(user: UserRegister, auth_service: AuthService = Depends(get_auth_service)):
    try:
        auth_service.register_user(user.username, user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    # Após o registro, autentica e retorna o token
    token = auth_service.authenticate_user(user.username, user.password)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user: UserLogin, auth_service: AuthService = Depends(get_auth_service)):
    token = auth_service.authenticate_user(user.username, user.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    return {"access_token": token, "token_type": "bearer"}
