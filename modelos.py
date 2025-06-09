# modelos.py
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from pathlib import Path

# Caminho para o banco
DB_PATH = Path(__file__).with_name("poa_olacefs.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Documento(Base):
    __tablename__ = 'documentos'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    ano = Column(String)
    orgao = Column(String)
    presidencia = Column(String)

    responsaveis = relationship("Responsavel", back_populates="documento")
    atividades = relationship("Atividade", back_populates="documento")
    alineamentos = relationship("Alineamento", back_populates="documento")
    recursos = relationship("Recurso", back_populates="documento")

class Responsavel(Base):
    __tablename__ = 'responsaveis'
    id = Column(Integer, primary_key=True)
    documento_id = Column(Integer, ForeignKey('documentos.id'))
    nome = Column(String)
    cargo = Column(String)
    email = Column(String)
    contato = Column(String)

    documento = relationship("Documento", back_populates="responsaveis")

class Atividade(Base):
    __tablename__ = 'atividades'
    id = Column(Integer, primary_key=True)
    documento_id = Column(Integer, ForeignKey('documentos.id'))
    meta = Column(String)
    atividade = Column(Text)
    objetivo = Column(Text)

    documento = relationship("Documento", back_populates="atividades")

class Alineamento(Base):
    __tablename__ = 'alineamentos'
    id = Column(Integer, primary_key=True)
    documento_id = Column(Integer, ForeignKey('documentos.id'))
    atividade_po = Column(String)
    meta_estrategica = Column(String)
    estrategia = Column(Text)

    documento = relationship("Documento", back_populates="alineamentos")

class Recurso(Base):
    __tablename__ = 'recursos'
    id = Column(Integer, primary_key=True)
    documento_id = Column(Integer, ForeignKey('documentos.id'))
    atividade = Column(Text)
    efs = Column(Float)
    olacefs = Column(Float)
    outros = Column(Float)
    total = Column(Float)

    documento = relationship("Documento", back_populates="recursos")

# Criar o banco se ainda não existir
def criar_banco():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    criar_banco()
