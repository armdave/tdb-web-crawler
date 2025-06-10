import pytest
from common.models import ExtractionJob, CrawlJob

def test_extraction_job_serialization_roundtrip():
    job = ExtractionJob(url="https://example.com", context="news")
    payload = job.to_json()
    restored = ExtractionJob.from_json(payload)
    assert job.url == restored.url
    assert job.context == restored.context

def test_crawl_job_to_from_json():
    original_job = CrawlJob(seed_urls=["https://example.com"], max_pages=100, num_workers=5)
    json_payload = original_job.to_json()
    deserialized_job = CrawlJob.from_json(json_payload)

    assert original_job.seed_urls == deserialized_job.seed_urls
    assert original_job.max_pages == deserialized_job.max_pages
    assert original_job.num_workers == deserialized_job.num_workers