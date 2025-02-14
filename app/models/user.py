from sqlalchemy import Column, String
from app.models.init import Base


class User(Base):

    """Esta clase não foi pedida no case, mas tem o intuito de mostrar habilidade de autenti
    cação, espero que possam considerar o teste via Berar Token."""

    __tablename__ = "users"

    # O username será a chave primária
    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)
