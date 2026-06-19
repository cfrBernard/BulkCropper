from pathlib import Path
import json


def list_folders(output_root: Path):
    if not output_root.exists():
        return []

    return sorted([p for p in output_root.iterdir() if p.is_dir()])


def load_folder(folder_path: Path):
    """
    Returns:
        images: list[Path]
        json_data: list[dict] | None
    """

    images = sorted(folder_path.glob("*.png"))

    json_file = folder_path / "brickognize.json"

    json_data = None

    if json_file.exists():
        with open(json_file, "r", encoding="utf-8") as f:
            json_data = json.load(f)

    return images, json_data


def normalize_items(items):
    if not items:
        return []

    normalized = []

    for i in items:
        if isinstance(i, dict):
            normalized.append({
                "id": i.get("id", ""),
                "name": i.get("name", ""),
                "bricklink": i.get("bricklink")
            })
        else:
            normalized.append({
                "id": str(i),
                "name": "",
                "bricklink": None
            })

    return normalized


def index_json(json_data):
    """
    Convert list -> dict for fast lookup by filename
    """

    if not json_data:
        return {}

    indexed = {}

    for item in json_data:
        indexed[item["input_id"]] = {
            "status": item.get("status", "UNKNOWN"),
            "items": normalize_items(item.get("items", []))
        }

    return indexed