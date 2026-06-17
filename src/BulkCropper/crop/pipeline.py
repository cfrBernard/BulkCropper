from pathlib import Path

from .config import Config
from .io import load_images
from .preprocessing import preprocess
from .detector import detect_objects
from .cropper import export_crops


def run_pipeline(args):

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
