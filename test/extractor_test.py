# File: test/test_extractor.py
import unittest
from unittest.mock import Mock, patch
from extractor import extract_and_save_content

class MockSaver:
    def __init__(self):
        self.saved = []

    def save(self, data):
        self.saved.append(data)

class TestExtractor(unittest.TestCase):

    @patch("extractor.extract_content")
    @patch("extractor.is_story_content", return_value=True)
    def test_extract_and_save_valid_story(self, mock_is_story, mock_extract):
        url = "https://example.com/story"
        expected_data = {
            "url": url,
            "domain": "example.com",
            "crawled_at": "2025-06-08T12:00:00Z",
            "published_at": None,
            "title": "Example Title",
            "body": "Example body.",
            "keywords": [],
            "link_to_images": []
        }
        mock_extract.return_value = expected_data

        saver = MockSaver()
        extract_and_save_content(url, saver)

        self.assertEqual(len(saver.saved), 1)
        self.assertEqual(saver.saved[0], expected_data)

    @patch("extractor.is_story_content", return_value=False)
    def test_extract_and_save_non_story(self, mock_is_story):
        url = "https://example.com/landing"
        saver = MockSaver()

        extract_and_save_content(url, saver)

        self.assertEqual(len(saver.saved), 0)

if __name__ == "__main__":
    unittest.main()