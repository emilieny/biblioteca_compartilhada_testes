# backend/factories/object_factory.py
# PADRÃO FACTORY METHOD
from backend.src.models.entities import Livro, Usuario, Emprestimo, Notificacao

class ObjectFactory:
    """
    Uma factory para criar objetos de domínio, desacoplando a criação de instâncias
    da lógica de negócio.
    """
    def create_livro(self, titulo, autor, isbn, ano_publicacao, id_doador, disponivel=True):
        return Livro(
            titulo=titulo,
            autor=autor,
            isbn=isbn,
            ano_publicacao=ano_publicacao,
            disponivel=disponivel,
            id_doador=id_doador
        )

    # CORRIGIDO: O método create_usuario agora aceita apenas 'nome', 'id_usuario', 'senha' e 'saldo_moedas'
    def create_usuario(self, nome, id_usuario, senha, email, saldo_moedas=0):
        return Usuario(
            nome=nome,
            id_usuario=id_usuario,
            senha=senha,
            email=email,
            saldo_moedas=saldo_moedas
        )

    def create_emprestimo(self, isbn_livro, id_usuario, duracao_dias=7):
        return Emprestimo(
            isbn_livro=isbn_livro,
            id_usuario=id_usuario,
            duracao_dias=duracao_dias
        )
    
    def create_notificacao(self, id_usuario: str, tipo_evento: str, mensagem: str, lida: bool = False):
        return Notificacao(
            id_usuario=id_usuario,
            tipo_evento=tipo_evento,
            mensagem=mensagem,
            lida=lida
        )