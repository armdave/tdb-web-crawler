import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from common.job_dispatcher import enqueue_extraction_job
from common.models import ExtractionJob, CrawlJob
from crawler.robots import can_fetch
from crawler.seed_urls import seed_urls

USER_AGENT = "DailyBriefingBot/1.0"

async def crawl_worker(queue: asyncio.Queue, max_pages: int, visited: set, session: aiohttp.ClientSession):
    while not queue.empty() and len(visited) < max_pages:
        if (len(visited) % 100 == 0):
            print('visited {} pages'.format(len(visited)))

        base_url = await queue.get()
        print('base_url: ', base_url)
        if base_url in visited:
            continue

        try:
            async with session.get(base_url, timeout=5) as res:
                if res.status != 200:
                    print("Failed for url {} with code {}".format(base_url, res.status))
                    continue  # TODO: retry logic

                visited.add(base_url)
                enqueue_extraction_job(ExtractionJob(url=base_url))

                # Extract links
                soup = BeautifulSoup(await res.text(), 'html.parser')
                for a_tag in soup.find_all('a', href=True):
                    raw_href = a_tag['href']
                    new_url = urljoin(base_url, raw_href)
                    parsed = urlparse(new_url)

                    if parsed.scheme not in ("http", "https"):
                        continue
                    if new_url in visited:
                        continue
                    if not can_fetch(new_url, USER_AGENT):
                        continue

                    await queue.put(new_url)

        except Exception as e:
            print(f"Failed to crawl {base_url}: {e}")
            continue

async def crawl_all_seed_urls(seed_list, max_pages: int, num_workers: int):
    queue = asyncio.Queue()
    visited = set()
    for url in seed_list:
        await queue.put(url)

    async with aiohttp.ClientSession(headers={"User-Agent": USER_AGENT}) as session:
        workers = [
            asyncio.create_task(crawl_worker(queue, max_pages, visited, session))
            for _ in range(num_workers)
        ]
        await asyncio.gather(*workers)

# Entry point for Pub/Sub-triggered job
async def run_crawl_job_from_payload(payload):
    job = CrawlJob.from_json(payload)

    seed_urls_param = job.seed_urls if job.seed_urls is not None else seed_urls
    max_pages = job.max_pages if job.max_pages is not None else 500
    num_workers = job.num_workers if job.num_workers is not None else 10

    await crawl_all_seed_urls(seed_urls_param, max_pages, num_workers)
