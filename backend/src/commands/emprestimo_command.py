# PADRÃO COMMAND

from abc import ABC, abstractmethod
from backend.src.services.biblioteca_service import BibliotecaService

class Command(ABC):
    """Interface base para todos os comandos."""
    @abstractmethod
    def execute(self):
        pass

class EmprestimoCommand(Command):
    """Comando para realizar um empréstimo de livro."""
    def __init__(self, service: BibliotecaService, id_usuario: str, isbn_livro: str):
        self.service = service
        self.id_usuario = id_usuario
        self.isbn_livro = isbn_livro
        self.success = False # Para rastrear o sucesso da operação

    def execute(self):
        self.success = self.service.realizar_emprestimo(self.id_usuario, self.isbn_livro)
        return self.success