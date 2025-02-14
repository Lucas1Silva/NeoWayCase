from datetime import timedelta
from app.repositories.user_repository import UserRepository
from app.utils.security import get_password_hash, verify_password, create_access_token

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expira em 30 minutos

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, username: str, password: str):
        # Verifica se o usuário já existe
        existing = self.user_repo.get_user_by_username(username)
        if existing:
            raise ValueError("Usuário já cadastrado")
        hashed = get_password_hash(password)
        return self.user_repo.create_user(username, hashed)

    def authenticate_user(self, username: str, password: str):
        user = self.user_repo.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        # Cria e retorna o token JWT
        access_token = create_access_token(
            data={"sub": username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return access_token
