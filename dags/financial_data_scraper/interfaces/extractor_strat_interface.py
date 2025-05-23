from abc import ABC, abstractmethod

class ExtractStrategy(ABC):
    @abstractmethod
    def extract(self):
        ...