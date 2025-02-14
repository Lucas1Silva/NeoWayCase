from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

# Configura o contexto para hashing de senha usando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Chave secreta para assinatura do JWT; em produção, usar variável de ambiente
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def get_password_hash(password: str) -> str:
    """
    Gera o hash da senha utilizando bcrypt.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha em texto plano corresponde ao hash armazenado.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Cria um token JWT com os dados fornecidos.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """
    Decodifica um token JWT, retornando os dados contidos.
    """
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except jwt.PyJWTError:
        return None
