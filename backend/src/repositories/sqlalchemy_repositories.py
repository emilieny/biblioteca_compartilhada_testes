# backend/repositories/sqlalchemy_repositories.py

# Importar db e os modelos das entidades
from backend.src.models.entities import Livro, Usuario, Emprestimo, Notificacao # Adicionar Notificacao
from backend.src.domain.ports import LivroRepository, UsuarioRepository, EmprestimoRepository, NotificacaoRepository # Adicionar NotificacaoRepository
from backend.src.extensions import db
from typing import Optional, List # <--- ATUALIZADO: Adicione List

class SQLAlchemyLivroRepository(LivroRepository):
    def get_all(self) -> List[Livro]:
        return Livro.query.all()

    def get_by_isbn(self, isbn: str) -> Optional[Livro]:
        return db.session.get(Livro, isbn)

    def add(self, livro: Livro) -> bool:
        if db.session.get(Livro, livro.isbn):
            return False
        db.session.add(livro)
        db.session.commit()
        return True

    def update(self, livro: Livro) -> bool:
        db.session.commit()
        return True

    def delete(self, isbn: str) -> bool:
        livro = db.session.get(Livro, isbn)
        if livro:
            db.session.delete(livro)
            db.session.commit()
            return True
        return False

class SQLAlchemyUsuarioRepository(UsuarioRepository):
    def get_all(self) -> List[Usuario]:
        return Usuario.query.all()

    def get_by_id(self, id_usuario: str) -> Optional[Usuario]:
        return db.session.get(Usuario, id_usuario)

    def add(self, usuario: Usuario) -> bool:
        if db.session.get(Usuario, usuario.id_usuario):
            return False
        db.session.add(usuario)
        db.session.commit()
        return True

    def update(self, usuario: Usuario) -> bool:
        db.session.commit()
        return True

    def delete(self, id_usuario: str) -> bool:
        usuario = db.session.get(Usuario, id_usuario)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return True
        return False

class SQLAlchemyEmprestimoRepository(EmprestimoRepository):
    def get_all(self) -> List[Emprestimo]:
        return Emprestimo.query.all()

    def get_by_id(self, emprestimo_id: int) -> Optional[Emprestimo]:
        return db.session.get(Emprestimo, emprestimo_id)

    def add(self, emprestimo: Emprestimo) -> bool:
        db.session.add(emprestimo)
        db.session.commit()
        return True

    def update(self, emprestimo: Emprestimo) -> bool:
        db.session.commit()
        return True

    def delete(self, emprestimo_id: int) -> bool:
        emprestimo = db.session.get(Emprestimo, emprestimo_id)
        if emprestimo:
            db.session.delete(emprestimo)
            db.session.commit()
            return True
        return False
    
    def get_emprestimo_ativo(self, isbn_livro: str, id_usuario: str) -> Optional[Emprestimo]:
        """
        Retorna o empréstimo ativo (não devolvido) de um livro específico
        por um usuário específico.
        """
        return Emprestimo.query.filter_by(isbn_livro=isbn_livro, id_usuario=id_usuario, data_devolucao=None).first()

class SQLAlchemyNotificacaoRepository(NotificacaoRepository): # <--- NOVA CLASSE DE REPOSITÓRIO: NotificacaoRepository
    def get_all(self) -> List[Notificacao]:
        return Notificacao.query.order_by(Notificacao.data_criacao.desc()).all()

    def get_by_id(self, notificacao_id: int) -> Optional[Notificacao]:
        return db.session.get(Notificacao, notificacao_id)
    
    def get_by_id_usuario(self, id_usuario: str) -> List[Notificacao]:
        return Notificacao.query.filter_by(id_usuario=id_usuario).order_by(Notificacao.data_criacao.desc()).all()

    def add(self, notificacao: Notificacao) -> bool:
        db.session.add(notificacao)
        db.session.commit()
        return True

    def update(self, notificacao: Notificacao) -> bool:
        db.session.commit()
        return True

    def delete(self, notificacao_id: int) -> bool:
        notificacao = db.session.get(Notificacao, notificacao_id)
        if notificacao:
            db.session.delete(notificacao)
            db.session.commit()
            return True
        return False