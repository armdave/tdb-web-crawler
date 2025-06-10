from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
from indexing.keyword_model import KeywordModel
from typing import List, Tuple

class KeyBERTKeywordModel(KeywordModel):
    def __init__(self):
        self.model = KeyBERT(SentenceTransformer("all-MiniLM-L6-v2"))

    def _chunk_text(self, text, chunk_size=1000, overlap=100):
        chunks = []
        i = 0
        while i < len(text):
            end = min(i + chunk_size, len(text))
            chunks.append(text[i:end])
            i += chunk_size - overlap
        return chunks

    def extract_keywords(self, text: str, top_n: int = 8) -> List[Tuple[str, float]]:
        chunks = self._chunk_text(text)
        all_keywords = []
        for chunk in chunks:
            keywords = self.model.extract_keywords(chunk, top_n=top_n, stop_words='english')
            all_keywords.extend(keywords)  # each is a (str, float) tuple

        seen = set()
        deduped_keywords = []
        for word, score in all_keywords:
            if word not in seen:
                deduped_keywords.append((word, score))
                seen.add(word)
            if len(deduped_keywords) == top_n:
                break

        return deduped_keywords
