from abc import ABC, abstractmethod

class KeywordModel(ABC):
    @abstractmethod
    def extract_keywords(self, text: str, top_n: int = 8) -> list[str]:
        pass
