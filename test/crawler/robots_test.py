import pytest
from unittest.mock import patch
from crawler.robots import can_fetch

@patch("crawler.robots.RobotFileParser.read")
@patch("crawler.robots.RobotFileParser.can_fetch", return_value=True)
def test_allow_all(mock_can_fetch, mock_read):
    assert can_fetch("https://example.com/page")

@patch("crawler.robots.RobotFileParser.read")
@patch("crawler.robots.RobotFileParser.can_fetch", return_value=False)
def test_disallow_all(mock_can_fetch, mock_read):
    assert not can_fetch("https://example.com/secret")

@patch("crawler.robots.RobotFileParser.read")
@patch("crawler.robots.RobotFileParser.can_fetch")
def test_disallow_specific_path(mock_can_fetch, mock_read):
    mock_can_fetch.side_effect = lambda agent, url: not url.startswith("https://example.com/private/")
    assert not can_fetch("https://example.com/private/data")
    assert can_fetch("https://example.com/public/page")

@patch("crawler.robots.RobotFileParser.read", side_effect=Exception("network error"))
def test_fetch_failure(mock_read):
    assert not can_fetch("https://example.com/failure")
