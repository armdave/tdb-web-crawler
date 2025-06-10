from google.cloud import firestore
from common.repository import Repository

import hashlib

class FirestoreRepository(Repository):

    def __init__(self):
        self.client = firestore.Client()

    def hash_url(self, url: str) -> str:
        return hashlib.sha256(url.encode("utf-8")).hexdigest()

    def save(self, data):
        url = data["url"]
        doc_id = self.hash_url(url)
        doc_ref = self.client.collection("datasources").document("default").collection("articles").document(doc_id)

        if not doc_ref.get().exists:
            doc_ref.set(data)
        else:
            print(f"Duplicate found for URL: {url}, skipping save.")
