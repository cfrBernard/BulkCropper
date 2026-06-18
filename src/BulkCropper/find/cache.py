import hashlib
import json
from pathlib import Path


class Cache:

    def __init__(self, cache_path: Path):

        self.cache_path = cache_path

        if cache_path.exists():

            self.data = json.loads(cache_path.read_text(encoding="utf8"))

        else:

            self.data = {}

    def compute_hash(self, image_path):

        h = hashlib.sha256()

        with open(image_path, "rb") as f:

            while True:

                b = f.read(8192)

                if not b:
                    break

                h.update(b)

        return h.hexdigest()

    def get(self, hash_):

        return self.data.get(hash_)

    def add(self, hash_, value):

        self.data[hash_] = value

    def save(self):

        self.cache_path.parent.mkdir(exist_ok=True, parents=True)

        self.cache_path.write_text(
            json.dumps(self.data, indent=4),
            encoding="utf8",
        )