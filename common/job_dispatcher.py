import os
from google.cloud import pubsub_v1
from common.models import ExtractionJob

PROJECT_ID = os.getenv("GCP_PROJECT")
EXTRACTION_TOPIC_ID = os.getenv("PUBSUB_EXTRACTION_TOPIC")

publisher = pubsub_v1.PublisherClient()
extraction_topic_path = publisher.topic_path(PROJECT_ID, EXTRACTION_TOPIC_ID)

def enqueue_extraction_job(job: ExtractionJob):
    publisher.publish(
        extraction_topic_path,
        job.to_json().encode("utf-8")
    )