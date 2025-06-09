import unittest
from models import ExtractionJob

class TestExtractionJob(unittest.TestCase):
    def test_serialization_roundtrip(self):
        job = ExtractionJob(url="https://example.com", context="news")
        payload = job.to_json()
        restored = ExtractionJob.from_json(payload)
        self.assertEqual(job.url, restored.url)
        self.assertEqual(job.context, restored.context)

if __name__ == '__main__':
    unittest.main()