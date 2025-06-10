from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from functools import lru_cache
import threading

_user_agent = 'DailyBriefingBot/1.0'
_robots_cache = {}
# _lock = threading.Lock()

def can_fetch(url, user_agent=_user_agent):
    parsed = urlparse(url)
    netloc = parsed.netloc
    scheme = parsed.scheme
    robots_url = f"{scheme}://{netloc}/robots.txt"

    # Check cache
    if netloc in _robots_cache:
        rp = _robots_cache[netloc]
    else:
        rp = RobotFileParser()
        rp.set_url(robots_url)
        try:
            rp.read()
            _robots_cache[netloc] = rp
        except:
            _robots_cache[netloc] = None
            return False  # be conservative

    if rp is None:
        return False

    return rp.can_fetch(user_agent, url)