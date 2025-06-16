# modelos.py
from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Float, ForeignKey,
    DateTime, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import uuid
from pathlib import Path

# ────────────── Configuração do banco ──────────────
DB_PATH = Path(__file__).with_name("poa_olacefs.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ────────────── Modelo de Lote ──────────────
class Lote(Base):
    __tablename__ = "lotes"
    id          = Column(Integer, primary_key=True)
    registro    = Column(String, default=lambda: uuid.uuid4().hex, unique=True)
    orgao       = Column(String)
    presidencia = Column(String)
    ano         = Column(String)
    status      = Column(String, default="EM_ANALISE")
    criado_em   = Column(DateTime, default=datetime.utcnow)

    documentos  = relationship("Documento", back_populates="lote", cascade="all, delete")

    __table_args__ = (
        UniqueConstraint("orgao", "ano", name="uix_orgao_ano"),
    )

# ────────────── Modelo de Documento ──────────────
class Documento(Base):
    __tablename__ = 'documentos'
    id          = Column(Integer, primary_key=True)
    lote_id     = Column(Integer, ForeignKey("lotes.id"))
    nome        = Column(String)
    ano         = Column(String)
    orgao       = Column(String)
    presidencia = Column(String)

    lote         = relationship("Lote", back_populates="documentos")
    responsaveis = relationship("Responsavel", back_populates="documento", cascade="all, delete")
    atividades   = relationship("Atividade", back_populates="documento", cascade="all, delete")
    alineamentos = relationship("Alineamento", back_populates="documento", cascade="all, delete")
    recursos     = relationship("Recurso", back_populates="documento", cascade="all, delete")

# ────────────── Modelo de Responsável ──────────────
class Responsavel(Base):
    __tablename__ = "responsaveis"
    id            = Column(Integer, primary_key=True)
    documento_id  = Column(Integer, ForeignKey("documentos.id"))
    nome          = Column(String)
    cargo         = Column(String)
    email         = Column(String)
    contato       = Column(String)

    documento     = relationship("Documento", back_populates="responsaveis")

# ────────────── Modelo de Atividade ──────────────
class Atividade(Base):
    __tablename__ = "atividades"
    id            = Column(Integer, primary_key=True)
    documento_id  = Column(Integer, ForeignKey("documentos.id"))
    meta          = Column(String)
    atividade     = Column(Text)
    objetivo      = Column(Text)

    documento     = relationship("Documento", back_populates="atividades")

# ────────────── Modelo de Alineamento ──────────────
class Alineamento(Base):
    __tablename__ = "alineamentos"
    id               = Column(Integer, primary_key=True)
    documento_id     = Column(Integer, ForeignKey("documentos.id"))
    atividade_po     = Column(String)
    meta_estrategica = Column(String)
    estrategia       = Column(String)

    documento        = relationship("Documento", back_populates="alineamentos")

# ────────────── Modelo de Recurso ──────────────
class Recurso(Base):
    __tablename__ = "recursos"
    id            = Column(Integer, primary_key=True)
    documento_id  = Column(Integer, ForeignKey("documentos.id"))
    atividade     = Column(String)
    efs           = Column(Float)
    olacefs       = Column(Float)
    outros        = Column(Float)
    total         = Column(Float)

    documento     = relationship("Documento", back_populates="recursos")

# ────────────── Criação do banco ──────────────
def criar_banco():
    Base.metadata.create_all(engine)

# ────────────── Utilitário: obter ou criar lote ──────────────
def obter_ou_criar_lote(session, orgao, ano, presidencia) -> Lote:
    # Tenta buscar um lote existente
    lote = session.query(Lote).filter_by(orgao=orgao, ano=ano).first()
    if lote:
        return lote  # já existe
    # Se não existe, cria um novo
    novo = Lote(orgao=orgao, ano=ano, presidencia=presidencia)
    session.add(novo)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Já existe um lote para esse órgão e ano.")
    return novo

# ────────────── Execução direta ──────────────
if __name__ == "__main__":
    criar_banco()
