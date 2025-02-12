from sqlalchemy.orm import Session
from app.models.client import Client

class ClientRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_client(self, client: Client):
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def get_client_by_document(self, document: str):
        return self.db.query(Client).filter(Client.document == document).first()

    def get_clients(self, name: str = None):
        query = self.db.query(Client)
        if name:
            query = query.filter(Client.name.ilike(f"%{name}%"))
        query = query.order_by(Client.name)
        return query.all()
