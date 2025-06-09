from google.cloud import firestore
from persistence import ArticleSaver

class FirestoreArticleSaver(ArticleSaver):

    def __init__(self):
        self.client = firestore.Client()

    def save(self, data):
        self.client.collection("datasources").document("default").collection("articles").add(data)
