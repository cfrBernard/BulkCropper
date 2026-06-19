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


def index_json(json_data):
    """
    Convert list -> dict for fast lookup by filename
    """

    if not json_data:
        return {}

    return {
        item["input_id"]: item
        for item in json_data
    }