from abc import ABC, abstractmethod
from typing import List, Tuple

class KeywordModel(ABC):
    @abstractmethod
    def extract_keywords(self, text: str, top_n: int = 8) -> List[Tuple[str, float]]:
        pass
