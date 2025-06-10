import json
from dataclasses import dataclass, asdict
from typing import List

@dataclass
class ExtractionJob:
    url: str
    context: str = ""

    def to_json(self):
        return json.dumps(asdict(self))

    @staticmethod
    def from_json(payload):
        data = json.loads(payload)
        return ExtractionJob(**data)
    

@dataclass
class CrawlJob:
    seed_urls: List[str]
    max_pages: int = 500
    num_workers: int = 10

    def to_json(self):
        return json.dumps(asdict(self))

    @staticmethod
    def from_json(payload):
        data = json.loads(payload)
        return CrawlJob(**data)
    
@dataclass
class IndexingJob:
    article_id: str

    def to_json(self):
        return json.dumps(asdict(self))

    @staticmethod
    def from_json(payload):
        data = json.loads(payload)
        return CrawlJob(**data)
