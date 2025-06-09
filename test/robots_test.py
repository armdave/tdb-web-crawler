import unittest
from unittest.mock import patch
from robots import can_fetch

class TestRobotsTxt(unittest.TestCase):

    @patch("robots.RobotFileParser.read")
    @patch("robots.RobotFileParser.can_fetch", return_value=True)
    def test_allow_all(self, mock_can_fetch, mock_read):
        self.assertTrue(can_fetch("https://example.com/page"))

    @patch("robots.RobotFileParser.read")
    @patch("robots.RobotFileParser.can_fetch", return_value=False)
    def test_disallow_all(self, mock_can_fetch, mock_read):
        self.assertFalse(can_fetch("https://example.com/secret"))

    @patch("robots.RobotFileParser.read")
    @patch("robots.RobotFileParser.can_fetch")
    def test_disallow_specific_path(self, mock_can_fetch, mock_read):
        mock_can_fetch.side_effect = lambda agent, url: \
            not url.startswith("https://example.com/private/")

        self.assertFalse(can_fetch("https://example.com/private/data"))
        self.assertTrue(can_fetch("https://example.com/public/page"))

    @patch("robots.RobotFileParser.read", side_effect=Exception("network error"))
    def test_fetch_failure(self, mock_read):
        self.assertFalse(can_fetch("https://example.com/failure"))

if __name__ == '__main__':
    unittest.main()