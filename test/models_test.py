import unittest
from models import ExtractionJob, CrawlJob

class TestExtractionJob(unittest.TestCase):
    def test_serialization_roundtrip(self):
        job = ExtractionJob(url="https://example.com", context="news")
        payload = job.to_json()
        restored = ExtractionJob.from_json(payload)
        self.assertEqual(job.url, restored.url)
        self.assertEqual(job.context, restored.context)


class TestCrawlJob(unittest.TestCase):
    def test_to_from_json(self):
        original_job = CrawlJob(seed_urls=["https://example.com"], max_pages=100, num_workers=5)
        json_payload = original_job.to_json()
        
        deserialized_job = CrawlJob.from_json(json_payload)
        
        self.assertEqual(original_job.seed_urls, deserialized_job.seed_urls)
        self.assertEqual(original_job.max_pages, deserialized_job.max_pages)
        self.assertEqual(original_job.num_workers, deserialized_job.num_workers)


if __name__ == '__main__':
    unittest.main()