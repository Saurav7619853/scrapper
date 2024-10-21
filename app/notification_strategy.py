from abc import ABC, abstractmethod

class NotificationStrategy(ABC):
    @abstractmethod
    def notify(self, message: str):
        pass
