import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from crawler import crawl_all_seed_urls, run_crawl_job_from_payload
from models import CrawlJob, ExtractionJob

class TestCrawler(unittest.IsolatedAsyncioTestCase):

    def make_mock_response(self, html, status=200):
        mock_response = AsyncMock()
        mock_response.status = status
        mock_response.text = AsyncMock(return_value=html)
        return mock_response

    @patch("crawler.enqueue_extraction_job")
    @patch("crawler.can_fetch")
    @patch("aiohttp.ClientSession.get")
    async def test_basic_crawl(self, mock_get, mock_can_fetch, mock_enqueue):
        html = """
            <html>
                <body>
                    <a href="http://example.com/page1">Page 1</a>
                    <a href="/page2">Page 2</a>
                    <a href="http://example.com/blocked">Blocked</a>
                </body>
            </html>
        """
        mock_get.return_value.__aenter__.return_value = self.make_mock_response(html)
        mock_can_fetch.side_effect = lambda url, ua: "blocked" not in url

        await crawl_all_seed_urls(["http://example.com"], max_pages=5, num_workers=1)

        # 3 URLs enqueued (seed + 2 non-blocked children)
        self.assertEqual(mock_enqueue.call_count, 3)
        called_urls = [call_args[0][0].url for call_args in mock_enqueue.call_args_list]
        self.assertIn("http://example.com", called_urls)
        self.assertIn("http://example.com/page1", called_urls)
        self.assertIn("http://example.com/page2", called_urls)
        self.assertNotIn("http://example.com/blocked", called_urls)

    @patch("crawler.crawl_all_seed_urls")
    async def test_run_crawl_job_from_payload_defaults(self, mock_crawl):
        payload = CrawlJob(seed_urls=None, max_pages=None, num_workers=None).to_json()
        await run_crawl_job_from_payload(payload)

        args = mock_crawl.call_args[0]
        self.assertIsInstance(args[0], list)
        self.assertEqual(args[1], 500)
        self.assertEqual(args[2], 10)

    @patch("crawler.enqueue_extraction_job")
    @patch("crawler.can_fetch", return_value=True)
    @patch("aiohttp.ClientSession.get")
    async def test_deduplication(self, mock_get, mock_can_fetch, mock_enqueue):
        html_seed = """
            <html>
                <body>
                    <a href="http://example.com/page1">Absolute</a>
                    <a href="http://example.com/page1">Duplicate</a>
                    <a href="/page1">Relative</a>
                </body>
            </html>
        """
        html_child = "<html></html>"

        def get_side_effect(url, **kwargs):
            mock_context = AsyncMock()
            if url == "http://example.com":
                mock_context.__aenter__.return_value = self.make_mock_response(html_seed)
            elif url == "http://example.com/page1":
                mock_context.__aenter__.return_value = self.make_mock_response(html_child)
            else:
                raise ValueError(f"Unexpected request to {url}")
            return mock_context

        mock_get.side_effect = get_side_effect

        await crawl_all_seed_urls(["http://example.com"], max_pages=10, num_workers=1)

        called_urls = [call_args[0][0].url for call_args in mock_enqueue.call_args_list]
        self.assertIn("http://example.com", called_urls)
        self.assertEqual(called_urls.count("http://example.com/page1"), 1)

        # Ensure each URL was fetched only once
        fetched_urls = [call_args[0][0] for call_args in mock_get.call_args_list]
        self.assertEqual(fetched_urls.count("http://example.com"), 1)
        self.assertEqual(fetched_urls.count("http://example.com/page1"), 1)

if __name__ == "__main__":
    unittest.main()
