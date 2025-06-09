from abc import ABC, abstractmethod

class ArticleSaver(ABC):

    @abstractmethod
    def save(self, data: dict):
        pass