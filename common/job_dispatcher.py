import os
from google.cloud import pubsub_v1
from common.models import ExtractionJob, IndexingJob

PROJECT_ID = os.getenv("GCP_PROJECT")
EXTRACTION_TOPIC_ID = os.getenv("PUBSUB_EXTRACTION_TOPIC")
INDEXING_TOPIC_ID = os.getenv("INDEXING_TOPIC")

publisher = pubsub_v1.PublisherClient()
extraction_topic_path = publisher.topic_path(PROJECT_ID, EXTRACTION_TOPIC_ID)
indexing_topic_path = publisher.topic_path(PROJECT_ID, INDEXING_TOPIC_ID)

def enqueue_extraction_job(job: ExtractionJob):
    publisher.publish(
        extraction_topic_path,
        job.to_json().encode("utf-8")
    )

def enqueue_indexing_job(job: IndexingJob):
    publisher.publish(
        indexing_topic_path,
        job.to_json().encode("utf-8")
    )