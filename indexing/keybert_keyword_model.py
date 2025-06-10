from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
from indexing.keyword_model import KeywordModel

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

    def extract_keywords(self, text: str, top_n: int = 8) -> list[str]:
        chunks = self._chunk_text(text)
        all_keywords = []
        for chunk in chunks:
            keywords = self.model.extract_keywords(chunk, top_n=top_n, stop_words='english')
            all_keywords.extend([kw[0] for kw in keywords])
        unique_keywords = list(dict.fromkeys(all_keywords))
        return unique_keywords[:top_n]
