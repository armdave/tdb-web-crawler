from abc import ABC, abstractmethod
from typing import List, Tuple

class Repository(ABC):

    @abstractmethod
    def retrieve_article(self, article_id: str) -> dict:
        pass
    
    @abstractmethod
    def save_article(self, data: dict):
        pass

    @abstractmethod
    def stream_articles(self):
        pass

    #TODO: pass the id, not doc. Ruins the interface
    @abstractmethod
    def update_article_keywords(self, article_id: str, keywords: List[Tuple[str, float]]) -> None:
        pass