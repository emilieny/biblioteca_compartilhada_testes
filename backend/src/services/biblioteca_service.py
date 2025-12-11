# backend/services/biblioteca_service.py

# PADRÃO REPOSITORY
# PADRÃO OBSERVER

from backend.src.domain.ports import LivroRepository, UsuarioRepository, EmprestimoRepository, NotificacaoRepository
from backend.src.models.entities import Livro, Usuario, Emprestimo
from datetime import datetime, timedelta
from backend.src.observers.subject import Subject
from backend.src.factories.object_factory import ObjectFactory
import bcrypt

class BibliotecaService(Subject):
    # Valores de Moedas
    MOEDAS_POR_DOACAO = 100
    MOEDAS_POR_EMPRESTIMO_LIVRO_DOADO = 50
    MOEDAS_POR_DIA_ATRASO = 10  # Moedas a serem perdidas por dia de atraso
    CUSTO_ALUGUEL_LIVRO = 50

    def __init__(self, livro_repo: LivroRepository, usuario_repo: UsuarioRepository, emprestimo_repo: EmprestimoRepository, notificacao_repo: NotificacaoRepository):
        super().__init__()
        self.livro_repo = livro_repo
        self.usuario_repo = usuario_repo
        self.emprestimo_repo = emprestimo_repo
        self.notificacao_repo = notificacao_repo
        self.object_factory = ObjectFactory()

    def adicionar_livro(self, livro: Livro):
        success = self.livro_repo.add(livro)
        if success:
            self.notify("livro_adicionado", {"isbn": livro.isbn, "titulo": livro.titulo})
        return success

    def cadastrar_usuario(self, usuario: Usuario):
        # A senha já foi tratada (hashed) na camada de app.py antes de chegar aqui.
        # A lógica de verificação de existência do usuário já é feita pelo repositório
        # ao tentar adicionar.
        success = self.usuario_repo.add(usuario)
        
        if success:
            self.notify("usuario_adicionado", {"id_usuario": usuario.id_usuario, "nome": usuario.nome})
            return {"message": "Usuário cadastrado com sucesso!"}, 201
        else:
            return {"error": "ID de usuário já existe."}, 409

    # NOVO: Método de autenticação modificado para receber a senha em texto plano
    def autenticar_usuario(self, id_usuario: str, senha: str):
        usuario = self.usuario_repo.get_by_id(id_usuario)
        if usuario:
            # NOVO: Verificar se a senha fornecida corresponde ao hash no banco de dados
            if bcrypt.checkpw(senha.encode('utf-8'), usuario.senha.encode('utf-8')):
                self.notify("usuario_autenticado", {"id_usuario": id_usuario})
                return usuario
        return None

    def doar_livro(self, livro: Livro, id_doador: str):
        usuario = self.usuario_repo.get_by_id(id_doador)
        if not usuario:
            return {"error": "Doador não encontrado."}, False

        livro.id_doador = id_doador
        success = self.livro_repo.add(livro)
        
        if success:
            usuario.saldo_moedas += self.MOEDAS_POR_DOACAO
            self.usuario_repo.update(usuario)
            self.notify("livro_doado", {"isbn": livro.isbn, "id_doador": id_doador, "titulo_livro": livro.titulo, "moedas_ganhas": self.MOEDAS_POR_DOACAO, "novo_saldo": usuario.saldo_moedas})
            return {"message": f"Livro '{livro.titulo}' doado com sucesso! Você ganhou {self.MOEDAS_POR_DOACAO} moedas. Saldo atual: {usuario.saldo_moedas} moedas."}, True
        else:
            return {"error": "Não foi possível adicionar o livro. Talvez o ISBN já exista."}, False

    def listar_livros_disponiveis(self):
        return [livro for livro in self.livro_repo.get_all() if livro.disponivel]

    def consultar_saldo_moedas(self, id_usuario: str):
        usuario = self.usuario_repo.get_by_id(id_usuario)
        if usuario:
            self.notify("saldo_consultado", {"id_usuario": id_usuario, "saldo": usuario.saldo_moedas})
            return {"id_usuario": usuario.id_usuario, "saldo_moedas": usuario.saldo_moedas}, True
        return {"error": "Usuário não encontrado."}, False

    def realizar_emprestimo(self, id_usuario: str, isbn_livro: str) -> bool:
        usuario = self.usuario_repo.get_by_id(id_usuario)
        livro = self.livro_repo.get_by_isbn(isbn_livro)

        if not usuario:
            self.notify("erro_emprestimo", {"id_usuario": id_usuario, "isbn_livro": isbn_livro, "motivo": "Usuário não encontrado"})
            return False
        if not livro or not livro.disponivel:
            self.notify("erro_emprestimo", {"id_usuario": id_usuario, "isbn_livro": isbn_livro, "motivo": "Livro não disponível"})
            return False
        
        # Verificar se o usuário tem saldo suficiente para alugar o livro
        if usuario.saldo_moedas < self.CUSTO_ALUGUEL_LIVRO:
            self.notify("erro_emprestimo", {"id_usuario": id_usuario, "isbn_livro": isbn_livro, "motivo": "Saldo insuficiente"})
            return False
        
        emprestimo_ativo = self.emprestimo_repo.get_emprestimo_ativo(isbn_livro, id_usuario)
        if emprestimo_ativo:
            self.notify("erro_emprestimo", {"id_usuario": id_usuario, "isbn_livro": isbn_livro, "motivo": "Livro já emprestado por este usuário"})
            return False

        emprestimo = self.object_factory.create_emprestimo(isbn_livro, id_usuario)

        if self.emprestimo_repo.add(emprestimo):
            livro.disponivel = False
            self.livro_repo.update(livro)
            
            # Descontar moedas do usuário que alugou o livro
            usuario.saldo_moedas -= self.CUSTO_ALUGUEL_LIVRO
            self.usuario_repo.update(usuario)

            if livro.id_doador and livro.id_doador != id_usuario:
                doador = self.usuario_repo.get_by_id(livro.id_doador)
                if doador:
                    doador.saldo_moedas += self.MOEDAS_POR_EMPRESTIMO_LIVRO_DOADO
                    self.usuario_repo.update(doador)
                    self.notify("livro_emprestado_doador", {
                        "id_doador": doador.id_usuario,
                        "titulo_livro": livro.titulo,
                        "id_locatario": id_usuario,
                        "moedas_ganhas": self.MOEDAS_POR_EMPRESTIMO_LIVRO_DOADO,
                        "novo_saldo": doador.saldo_moedas
                    })

            self.notify("livro_emprestado", {
                "id_usuario": id_usuario,
                "isbn_livro": isbn_livro,
                "titulo_livro": livro.titulo,
                "data_devolucao_prevista": emprestimo.data_devolucao_prevista.isoformat(),
                "moedas_descontadas": self.CUSTO_ALUGUEL_LIVRO,
                "novo_saldo": usuario.saldo_moedas
            })
            return True
        return False

    def devolver_livro(self, id_usuario: str, isbn_livro: str):
        emprestimo = self.emprestimo_repo.get_emprestimo_ativo(isbn_livro, id_usuario)
        livro = self.livro_repo.get_by_isbn(isbn_livro)
        usuario = self.usuario_repo.get_by_id(id_usuario)

        if not emprestimo:
            return {"error": "Empréstimo não encontrado ou já devolvido."}, False
        if not livro:
            return {"error": "Livro não encontrado."}, False
        if not usuario:
            return {"error": "Usuário não encontrado."}, False

        emprestimo.data_devolucao = datetime.now()
        
        if self.emprestimo_repo.update(emprestimo):
            livro.disponivel = True
            self.livro_repo.update(livro)

            dias_atraso = (emprestimo.data_devolucao - emprestimo.data_devolucao_prevista).days
            if dias_atraso > 0:
                moedas_perdidas = dias_atraso * self.MOEDAS_POR_DIA_ATRASO
                if usuario.saldo_moedas >= moedas_perdidas:
                    usuario.saldo_moedas -= moedas_perdidas
                    self.usuario_repo.update(usuario)
                    self.notify("penalidade_aplicada", {"id_usuario": id_usuario, "isbn_livro": isbn_livro, "dias_atraso": dias_atraso, "moedas_perdidas": moedas_perdidas, "novo_saldo": usuario.saldo_moedas})
                    return {"message": f"Livro devolvido com sucesso! Penalidade de {moedas_perdidas} moedas aplicada por {dias_atraso} dias de atraso. Saldo atual: {usuario.saldo_moedas} moedas."}, True
                else:
                    moedas_perdidas_reais = usuario.saldo_moedas
                    usuario.saldo_moedas = 0
                    self.usuario_repo.update(usuario)
                    self.notify("penalidade_parcialmente_aplicada", {"id_usuario": id_usuario, "isbn_livro": isbn_livro, "dias_atraso": dias_atraso, "moedas_perdidas": moedas_perdidas_reais, "novo_saldo": usuario.saldo_moedas})
                    return {"message": f"Livro devolvido com sucesso! Penalidade de {moedas_perdidas} moedas aplicada por {dias_atraso} dias de atraso. Saldo insuficiente para cobrir total. Saldo zerado. Saldo atual: {usuario.saldo_moedas} moedas."}, True
        
            self.notify("livro_devolvido", {
                "id_usuario": id_usuario, 
                "isbn_livro": isbn_livro, 
                "titulo_livro": livro.titulo
            })
            return {"message": "Livro devolvido com sucesso!", "saldo_atual": usuario.saldo_moedas}, True
        return {"error": "Não foi possível registrar a devolução."}, False