from app.notification_strategy import NotificationStrategy

class ConsoleNotification(NotificationStrategy):
    def notify(self, message: str):
        print(f"Notification: {message}")
