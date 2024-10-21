from abc import ABC, abstractmethod

class StorageStrategy(ABC):
    @abstractmethod
    def save(self, data):
        pass
