# PADRÃO OBSERVER

from backend.src.observers.log_observer import Observer # Esta importação será corrigida na próxima etapa

class Subject:
    """Classe base para objetos que podem ser observados."""
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        """Anexa um observador ao sujeito."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        """Desanexa um observador do sujeito."""
        self._observers.remove(observer)

    def notify(self, event_type: str, data: dict):
        """Notifica todos os observadores sobre um evento."""
        for observer in self._observers:
            observer.update(event_type, data)