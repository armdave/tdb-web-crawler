import json
from dataclasses import dataclass, asdict

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