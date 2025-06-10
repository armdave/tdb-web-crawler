import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
from common.persistence import ArticleSaver

def is_story_content(soup):
    paragraphs = soup.find_all('p')
    content = [p.get_text(strip=True) for p in paragraphs]
    return len(' '.join(content)) > 1500

def extract_content(url):
    try:
        res = requests.get(url, timeout=5)
        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, 'html.parser')
        if not is_story_content(soup):
            print("URL {} deemed aggregator page".format(url))
            return None

        title = soup.title.string if soup.title else ""
        body = ' '.join(p.get_text() for p in soup.find_all('p'))
        images = [img['src'] for img in soup.find_all('img', src=True)]

        data = {
            "url": url,
            "domain": urlparse(url).netloc,
            "crawled_at": datetime.utcnow().isoformat(),
            "published_at": None,
            "title": title,
            "body": body,
            "keywords": [],
            "link_to_images": images
        }
        return data
    except:
        return None
    
def extract_and_save_content(url, saver: ArticleSaver):
    url_content = extract_content(url)
    if url_content:
        saver.save(url_content)
