from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Usuario(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)

    # perfil do usuario: "adimin" ou "operador"
    role = Column(String(20), nullable=False, default="operador")

    # permite desativar sem excluir do db
    ativo = Column(Boolean, default=True)
    criando_em = Column(DateTime, server_default=func.now())