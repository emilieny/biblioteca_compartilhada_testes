# PADRÃO STRATEGY

from abc import ABC, abstractmethod

class NotificationStrategy(ABC):
    """Interface base para estratégias de notificação."""
    @abstractmethod
    def send_notification(self, user_name: str, message: str):
        pass

class EmailNotification(NotificationStrategy):
    """Estratégia de notificação por e-mail."""
    def send_notification(self, user_name: str, message: str):
        print(f"[Email] Enviando e-mail para {user_name}: '{message}'")
        # Lógica real de envio de e-mail aqui (via SMTP, API, etc.)

class SMSNotification(NotificationStrategy):
    """Estratégia de notificação por SMS."""
    def send_notification(self, user_name: str, message: str):
        print(f"[SMS] Enviando SMS para {user_name}: '{message}'")
        # Lógica real de envio de SMS aqui (via API de SMS, etc.)

class PushNotification(NotificationStrategy):
    """Estratégia de notificação por Push (app)."""
    def send_notification(self, user_name: str, message: str):
        print(f"[Push] Enviando notificação push para {user_name}: '{message}'")
        # Lógica real de envio de push aqui