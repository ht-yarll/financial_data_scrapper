from abc import ABC, abstractmethod

class LoadStrategy(ABC):
    @abstractmethod
    def load(self):
        ...