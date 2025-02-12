from app.repositories.client_repository import ClientRepository
from app.models.client import Client
from app.utils.validators import is_valid_document

class ClientService:
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    def create_client(self, document: str, name: str, is_blocked: bool = False):
        # Validação do documento (CPF/CNPJ)
        if not is_valid_document(document):
            raise ValueError("Documento inválido")

        # Verifica se o cliente já existe
        existing = self.repository.get_client_by_document(document)
        if existing:
            raise ValueError("Cliente já cadastrado")

        client = Client(document=document, name=name, is_blocked=is_blocked)
        return self.repository.create_client(client)

    def get_client(self, document: str):
        return self.repository.get_client_by_document(document)

    def get_clients(self, name: str = None):
        return self.repository.get_clients(name)
