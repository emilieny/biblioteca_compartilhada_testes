# backend/models/entities.py
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta, timezone
from backend.src.extensions import db
from sqlalchemy.sql import func

# Base de Dados
class Livro(db.Model):
    __tablename__ = 'livros'
    isbn = Column(String(13), primary_key=True)
    titulo = Column(String(255), nullable=False)
    autor = Column(String(255), nullable=False)
    ano_publicacao = Column(Integer, nullable=False)
    disponivel = Column(Boolean, default=True)
    id_doador = Column(String(50), ForeignKey('usuarios.id_usuario'))

    # CORRIGIDO: timezone-aware datetime
    data_doacao = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    doador = relationship('Usuario', back_populates='livros_doados')
    emprestimos = relationship('Emprestimo', back_populates='livro')

    def __init__(self, titulo, autor, isbn, ano_publicacao, disponivel=True, id_doador=None):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.ano_publicacao = ano_publicacao
        self.disponivel = disponivel
        self.id_doador = id_doador

    def to_dict(self):
        return {
            'isbn': self.isbn,
            'titulo': self.titulo,
            'autor': self.autor,
            'ano_publicacao': self.ano_publicacao,
            'disponivel': self.disponivel,
            'data_doacao': self.data_doacao.isoformat() if self.data_doacao else None
        }


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = Column(String(50), primary_key=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    saldo_moedas = Column(Integer, default=100)

    # CORRIGIDO
    data_cadastro = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    livros_doados = relationship('Livro', back_populates='doador')
    emprestimos = relationship('Emprestimo', back_populates='usuario_emprestimo')
    notificacoes = relationship('Notificacao', back_populates='usuario_notificacao')

    def __init__(self, nome, id_usuario, senha, email, saldo_moedas=100):
        self.nome = nome
        self.id_usuario = id_usuario
        self.senha = senha
        self.email = email
        self.saldo_moedas = saldo_moedas

    def to_dict(self):
        return {
            'id_usuario': self.id_usuario,
            'nome': self.nome,
            'email': self.email,
            'saldo_moedas': self.saldo_moedas
        }


class Emprestimo(db.Model):
    __tablename__ = 'emprestimos'
    id = Column(Integer, primary_key=True)
    id_usuario = Column(String(50), ForeignKey('usuarios.id_usuario'), nullable=False)
    isbn_livro = Column(String(13), ForeignKey('livros.isbn'), nullable=False)
    data_emprestimo = Column(DateTime(timezone=True), server_default=func.now())
    data_devolucao_prevista = Column(DateTime(timezone=True))
    data_devolucao = Column(DateTime(timezone=True))
    status = Column(String(50), default='Ativo')

    usuario_emprestimo = relationship('Usuario', back_populates='emprestimos')
    livro = relationship('Livro', back_populates='emprestimos')

    def __init__(self, isbn_livro, id_usuario, duracao_dias=7):
        self.isbn_livro = isbn_livro
        self.id_usuario = id_usuario

        # CORRIGIDO
        now = datetime.now(timezone.utc)
        self.data_emprestimo = now
        self.data_devolucao_prevista = now + timedelta(days=duracao_dias)

    def to_dict(self):
        return {
            'id': self.id,
            'id_usuario': self.id_usuario,
            'isbn_livro': self.isbn_livro,
            'data_emprestimo': self.data_emprestimo.isoformat() if self.data_emprestimo else None,
            'data_devolucao_prevista': self.data_devolucao_prevista.isoformat() if self.data_devolucao_prevista else None,
            'data_devolucao': self.data_devolucao.isoformat() if self.data_devolucao else None,
            'status': self.status
        }


class Notificacao(db.Model):
    __tablename__ = 'notificacoes'
    id = Column(Integer, primary_key=True)
    id_usuario = Column(String(50), ForeignKey('usuarios.id_usuario'), nullable=False)
    mensagem = Column(String(500), nullable=False)
    tipo_evento = Column(String(50), nullable=False)

    # CORRIGIDO
    data_criacao = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    lida = Column(Boolean, default=False)

    usuario_notificacao = relationship('Usuario', back_populates='notificacoes')

    def __init__(self, id_usuario: str, tipo_evento: str, mensagem: str, lida: bool = False):
        self.id_usuario = id_usuario
        self.tipo_evento = tipo_evento
        self.mensagem = mensagem
        self.lida = lida

    def to_dict(self):
        return {
            'id': self.id,
            'id_usuario': self.id_usuario,
            'mensagem': self.mensagem,
            'tipo_evento': self.tipo_evento,
            'data_criacao': self.data_criacao.isoformat(),
            'lida': self.lida
        }
