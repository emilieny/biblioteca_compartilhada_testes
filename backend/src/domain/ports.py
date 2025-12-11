# backend/domain/ports.py

from abc import ABC, abstractmethod
from typing import List, Optional
# As entidades serão importadas dos seus modelos
# Estes imports aqui são apenas para Type Hinting nas interfaces
from backend.src.models.entities import Livro, Usuario, Emprestimo, Notificacao # Adicionar Notificacao

class LivroRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Livro]:
        pass

    @abstractmethod
    def get_by_isbn(self, isbn: str) -> Optional[Livro]:
        pass

    @abstractmethod
    def add(self, livro: Livro) -> bool:
        pass

    @abstractmethod
    def update(self, livro: Livro) -> bool:
        pass

    @abstractmethod
    def delete(self, isbn: str) -> bool:
        pass

class UsuarioRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Usuario]:
        pass

    @abstractmethod
    def get_by_id(self, id_usuario: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def add(self, usuario: Usuario) -> bool:
        pass

    @abstractmethod
    def update(self, usuario: Usuario) -> bool:
        pass

    @abstractmethod
    def delete(self, id_usuario: str) -> bool:
        pass

class EmprestimoRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Emprestimo]:
        pass

    @abstractmethod
    def get_by_id(self, emprestimo_id: int) -> Optional[Emprestimo]:
        pass

    @abstractmethod
    def add(self, emprestimo: Emprestimo) -> bool:
        pass

    @abstractmethod
    def update(self, emprestimo: Emprestimo) -> bool:
        pass

    @abstractmethod
    def delete(self, emprestimo_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_emprestimo_ativo(self, isbn_livro: str, id_usuario: str) -> Optional[Emprestimo]:
        pass

class NotificacaoRepository(ABC): # <--- NOVO: Interface para NotificacaoRepository
    @abstractmethod
    def get_all(self) -> List[Notificacao]:
        pass

    @abstractmethod
    def get_by_id(self, notificacao_id: int) -> Optional[Notificacao]:
        pass

    @abstractmethod
    def get_by_id_usuario(self, id_usuario: str) -> List[Notificacao]:
        pass

    @abstractmethod
    def add(self, notificacao: Notificacao) -> bool:
        pass

    @abstractmethod
    def update(self, notificacao: Notificacao) -> bool:
        pass

    @abstractmethod
    def delete(self, notificacao_id: int) -> bool:
        pass