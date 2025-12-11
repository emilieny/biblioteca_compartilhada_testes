# backend/observers/log_observer.py

from abc import ABC, abstractmethod
from backend.src.domain.ports import NotificacaoRepository
from backend.src.factories.object_factory import ObjectFactory
from datetime import datetime

class Observer(ABC):
    """Interface base para os observadores."""
    @abstractmethod
    def update(self, *args, **kwargs):
        pass

class LogObserver(Observer):
    """Um observador que registra eventos em um log e salva notificações no DB."""
    def __init__(self, notificacao_repo: NotificacaoRepository, object_factory: ObjectFactory):
        self.notificacao_repo = notificacao_repo
        self.object_factory = object_factory

    def update(self, event_type: str, data: dict):
        print(f"[LOG OBSERVER] Evento '{event_type}' ocorrido com dados: {data}")

        # Lógica para salvar notificações específicas no banco de dados
        if event_type == "livro_emprestado_doador":
            id_doador = data.get("id_doador")
            titulo_livro = data.get("titulo_livro")
            id_locatario = data.get("id_locatario")
            moedas_ganhas = data.get("moedas_ganhas")
            if id_doador:
                mensagem = f"Seu livro '{titulo_livro}' foi alugado por {id_locatario}! Você ganhou {moedas_ganhas} moedas."
                notificacao = self.object_factory.create_notificacao(id_doador, event_type, mensagem)
                self.notificacao_repo.add(notificacao)

        elif event_type == "penalidade_aplicada":
            id_usuario = data.get("id_usuario")
            isbn_livro = data.get("isbn_livro")
            moedas_perdidas = data.get("moedas_perdidas")
            if id_usuario:
                mensagem = f"Penalidade aplicada! Você perdeu {moedas_perdidas} moedas pelo atraso do livro {titulo_livro}."
                notificacao = self.object_factory.create_notificacao(id_usuario, event_type, mensagem)
                self.notificacao_repo.add(notificacao)
        
        elif event_type == "penalidade_parcialmente_aplicada":
            id_usuario = data.get("id_usuario")
            isbn_livro = data.get("isbn_livro")
            moedas_perdidas = data.get("moedas_perdidas")
            if id_usuario:
                mensagem = f"Penalidade parcial! Você perdeu {moedas_perdidas} moedas pelo atraso do livro {titulo_livro}. Saldo zerado."
                notificacao = self.object_factory.create_notificacao(id_usuario, event_type, mensagem)
                self.notificacao_repo.add(notificacao)

        elif event_type == "usuario_adicionado":
            id_usuario = data.get("id_usuario")
            nome = data.get("nome")
            if id_usuario:
                mensagem = f"Bem-vindo(a), {nome}! Seu cadastro foi realizado com sucesso. Doe um livro e ganhe moedas!"
                notificacao = self.object_factory.create_notificacao(id_usuario, event_type, mensagem)
                self.notificacao_repo.add(notificacao)

        elif event_type == "livro_doado":
            id_doador = data.get("id_doador")
            isbn = data.get("isbn")
            titulo_livro = data.get("titulo_livro")
            moedas_ganhas = data.get("moedas_ganhas")
            if id_doador:
                mensagem = f"Obrigado por doar o livro '{titulo_livro}'! Você ganhou {moedas_ganhas} moedas."
                notificacao = self.object_factory.create_notificacao(id_doador, event_type, mensagem)
                self.notificacao_repo.add(notificacao)
        
        elif event_type == "livro_emprestado":
            id_usuario = data.get("id_usuario")
            isbn_livro = data.get("isbn_livro")
            titulo_livro = data.get("titulo_livro") 
            data_devolucao_prevista = data.get("data_devolucao_prevista")
            moedas_descontadas = data.get("moedas_descontadas") 
            novo_saldo = data.get("novo_saldo")
            
            if id_usuario and titulo_livro and data_devolucao_prevista: # Adicionada verificação para titulo_livro
                try:
                    data_obj = datetime.fromisoformat(data_devolucao_prevista)
                    data_formatada = data_obj.strftime("%d/%m/%Y")
                except ValueError:
                    data_formatada = "data inválida"
                
                mensagem = f"Você alugou o livro '{titulo_livro}' com sucesso! {moedas_descontadas} moedas foram descontadas. Seu novo saldo é: {novo_saldo} moedas! Devolução prevista para: {data_formatada}."
                notificacao = self.object_factory.create_notificacao(id_usuario, event_type, mensagem)
                self.notificacao_repo.add(notificacao)

        elif event_type == "livro_devolvido":
            id_usuario = data.get("id_usuario")
            isbn_livro = data.get("isbn_livro")
            titulo_livro = data.get("titulo_livro") # <--- Corrigido aqui
            if id_usuario and titulo_livro: # Adicionada verificação para titulo_livro
                mensagem = f"Você devolveu o livro '{titulo_livro}' com sucesso!" 
                notificacao = self.object_factory.create_notificacao(id_usuario, event_type, mensagem)
                self.notificacao_repo.add(notificacao)