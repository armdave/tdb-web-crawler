from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

def can_fetch(url, user_agent='TDBBot'):
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    rp = RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
        return rp.can_fetch(user_agent, url)
    except:
        return False  # be conservative if anything fails