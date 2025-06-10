from google.cloud import firestore
from google.cloud.firestore_v1 import DocumentSnapshot
from common.repository import Repository
from typing import List, Tuple

import hashlib

class FirestoreRepository(Repository):

    def __init__(self):
        self.client = firestore.Client()

    def hash_url(self, url: str) -> str:
        return hashlib.sha256(url.encode("utf-8")).hexdigest()
    
    def retrieve_article(self, article_id: str) -> dict:
        doc_ref = self.client.collection("datasources").document("default").collection("articles").document(article_id)
        doc_snapshot = doc_ref.get()

        if not doc_snapshot.exists:
            raise ValueError(f"Article with ID '{article_id}' not found.")

        return doc_snapshot.to_dict()

    def save_article(self, data):
        url = data["url"]
        doc_id = self.hash_url(url)
        doc_ref = self.client.collection("datasources").document("default").collection("articles").document(doc_id)

        if not doc_ref.get().exists:
            doc_ref.set(data)
        else:
            print(f"Duplicate found for URL: {url}, skipping save.")

    def stream_articles(self):
        collection_ref = self.client.collection("datasources").document("default").collection("articles")
        return collection_ref.stream()
    
    def update_article_keywords(self, article_id: str, keywords: List[Tuple[str, float]]) -> None:
        doc_ref = self.client.collection("datasources").document("default").collection("articles").document(article_id)
        formatted = [{"keyword": kw, "score": score} for kw, score in keywords]
        doc_ref.update({"keywords": formatted})
