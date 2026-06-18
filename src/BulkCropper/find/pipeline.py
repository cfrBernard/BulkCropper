import json
import time
from collections import defaultdict

from .api import predict
from .cache import Cache
from .config import Config
from .io import load_images


# ----------------------------
# CLEAN PARSER
# ----------------------------
def extract_bricklink(item):

    bricklink = None

    for ext in item.get("external_sites", []):
        if ext.get("name", "").lower() == "bricklink":
            bricklink = ext.get("url")
            break

    return {
        "id": item.get("id"),
        "name": item.get("name"),
        "bricklink": bricklink
    }


# ----------------------------
# PIPELINE
# ----------------------------
def run_pipeline(args):

    cfg = Config()

    print(cfg.output_root.resolve())

    jobs = load_images(cfg)
    cache = Cache(cfg.cache_file)

    print(f"{len(jobs)} images to process")

    results_by_folder = defaultdict(list)

    start = time.time()

    seen = set()
    empty_count = 0

    for i, job in enumerate(jobs, start=1):

        image = job["image"]
        folder = job["folder"]

        image_hash = cache.compute_hash(image)

        result = cache.get(image_hash)
        from_cache = result is not None

        if result is None:
            result = predict(cfg, image)
            cache.add(image_hash, result)
            cache.save()
            time.sleep(cfg.sleep_between_requests)

        items = result.get("items", [])
        nb_items = len(items)

        # ----------------------------
        # BUILD IMAGE ENTRY (NEW)
        # ----------------------------
        image_entry = {
            "folder": folder.name,
            "input_id": image.name,
            "status": None,
            "items": []
        }

        # ----------------------------
        # STATUS LOGIC
        # ----------------------------
        if nb_items == 0:
            image_entry["status"] = "NOT_FOUND"
            image_entry["items"] = "not found"
            empty_count += 1
            status_log = "⚠️ EMPTY"
        else:
            image_entry["status"] = "OK"

            status_log = "🟢 CACHE" if from_cache else "🔴 API"

            for item in items:

                key = (folder.name, item.get("id"))

                if key in seen:
                    continue
                seen.add(key)

                image_entry["items"].append(
                    extract_bricklink(item)
                )

        # ----------------------------
        # STORE PER FOLDER
        # ----------------------------
        results_by_folder[folder.name].append(image_entry)

        # ----------------------------
        # PROGRESS
        # ----------------------------
        elapsed = time.time() - start
        avg = elapsed / i
        remaining = len(jobs) - i
        eta = avg * remaining

        print(
            f"[{i}/{len(jobs)}] "
            f"{status_log} "
            f"{image.name} "
            f"(items={nb_items}) "
            f"ETA={eta:.0f}s"
        )

    # ----------------------------
    # WRITE 1 JSON PER FOLDER
    # ----------------------------
    for folder_name, items in results_by_folder.items():

        out_path = cfg.output_root / folder_name / "brickognize.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)

        with open(out_path, "w", encoding="utf8") as f:
            json.dump(items, f, indent=4, ensure_ascii=False)

    print("✅ Process completed.")
    print(f"⚠️ Not found: {empty_count}/{len(jobs)}")