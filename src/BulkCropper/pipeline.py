from pathlib import Path

from .core.config import Config
from .core.io import load_images
from .core.preprocessing import preprocess
from .core.detector import detect_objects
from .core.cropper import export_crops


def run_pipeline():

    cfg = Config()

    images = load_images(cfg)

    for image_path, image in images:

        print(f"Processing : {image_path.name}")

        processed, debug = preprocess(image, cfg)

        boxes = detect_objects(processed, cfg, debug)

        export_crops(
            image,
            image_path,
            boxes,
            processed,
            cfg,
            debug,
        )