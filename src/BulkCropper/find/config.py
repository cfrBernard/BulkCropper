from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:

    output_root: Path = Path("data/output")

    json_name: str = "brickognize.json"

    cache_file: Path = Path("data/brickognize_cache.json")

    api_url: str = "https://api.brickognize.com/predict/"

    sleep_between_requests: float = 1.5