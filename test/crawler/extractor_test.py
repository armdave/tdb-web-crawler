import pytest
from unittest.mock import patch
from crawler.extractor import extract_and_save_content

class MockRepository:
    def __init__(self):
        self.saved = []

    def save(self, data):
        self.saved.append(data)

@patch("crawler.extractor.extract_content")
@patch("crawler.extractor.is_story_content", return_value=True)
def test_extract_and_save_valid_story(mock_is_story, mock_extract):
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

    saver = MockRepository()
    extract_and_save_content(url, saver)

    assert len(saver.saved) == 1
    assert saver.saved[0] == expected_data

@patch("crawler.extractor.is_story_content", return_value=False)
def test_extract_and_save_non_story(mock_is_story):
    url = "https://example.com/landing"
    saver = MockRepository()

    extract_and_save_content(url, saver)

    assert len(saver.saved) == 0
