import pytest
from unittest.mock import patch, AsyncMock
from crawler.crawler import crawl_all_seed_urls, run_crawl_job_from_payload
from common.models import CrawlJob

@pytest.fixture
def make_mock_response():
    def _make_mock_response(html, status=200):
        mock_response = AsyncMock()
        mock_response.status = status
        mock_response.text = AsyncMock(return_value=html)
        return mock_response
    return _make_mock_response

@pytest.mark.asyncio
@patch("crawler.crawler.enqueue_extraction_job")
@patch("crawler.crawler.can_fetch")
@patch("aiohttp.ClientSession.get")
async def test_basic_crawl(mock_get, mock_can_fetch, mock_enqueue, make_mock_response):
    html = """
        <html>
            <body>
                <a href="http://example.com/page1">Page 1</a>
                <a href="/page2">Page 2</a>
                <a href="http://example.com/blocked">Blocked</a>
            </body>
        </html>
    """
    mock_get.return_value.__aenter__.return_value = make_mock_response(html)
    mock_can_fetch.side_effect = lambda url, ua: "blocked" not in url

    await crawl_all_seed_urls(["http://example.com"], max_pages=5, num_workers=1)

    # Seed + 2 valid children
    assert mock_enqueue.call_count == 3
    called_urls = [call_args[0][0].url for call_args in mock_enqueue.call_args_list]
    assert "http://example.com" in called_urls
    assert "http://example.com/page1" in called_urls
    assert "http://example.com/page2" in called_urls
    assert "http://example.com/blocked" not in called_urls

@pytest.mark.asyncio
@patch("crawler.crawler.crawl_all_seed_urls")
async def test_run_crawl_job_from_payload_defaults(mock_crawl):
    payload = CrawlJob(seed_urls=None, max_pages=None, num_workers=None).to_json()
    await run_crawl_job_from_payload(payload)

    args = mock_crawl.call_args[0]
    assert isinstance(args[0], list)
    assert args[1] == 500
    assert args[2] == 10

@pytest.mark.asyncio
@patch("crawler.crawler.enqueue_extraction_job")
@patch("crawler.crawler.can_fetch", return_value=True)
@patch("aiohttp.ClientSession.get")
async def test_deduplication(mock_get, mock_can_fetch, mock_enqueue, make_mock_response):
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
            mock_context.__aenter__.return_value = make_mock_response(html_seed)
        elif url == "http://example.com/page1":
            mock_context.__aenter__.return_value = make_mock_response(html_child)
        else:
            raise ValueError(f"Unexpected request to {url}")
        return mock_context

    mock_get.side_effect = get_side_effect

    await crawl_all_seed_urls(["http://example.com"], max_pages=10, num_workers=1)

    called_urls = [call_args[0][0].url for call_args in mock_enqueue.call_args_list]
    assert "http://example.com" in called_urls
    assert called_urls.count("http://example.com/page1") == 1

    fetched_urls = [call_args[0][0] for call_args in mock_get.call_args_list]
    assert fetched_urls.count("http://example.com") == 1
    assert fetched_urls.count("http://example.com/page1") == 1
