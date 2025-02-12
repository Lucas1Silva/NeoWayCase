from sqlalchemy import Column, String, Boolean
from app.models.init import Base


class Client(Base):
    __tablename__ = "clients"

    document = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    is_blocked = Column(Boolean, default=False)
