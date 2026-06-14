import os

from .core.config import Config
from .core.detector import detect_objects
from .core.cropper import crop_objects
from .core.utils import (
    load_image,
    save_crops,
    save_debug_image,
    ensure_dir,
)


def run_pipeline(input_path, output_path, debug=False,
                 padding=20, min_area=400, size=512):

    cfg = Config(
        debug=debug,
        padding=padding,
        min_area=min_area,
        output_size=size,
        input_path=input_path,
        output_path=output_path,
    )

    ensure_dir(cfg.output_path)

    image = load_image(cfg.input_path)

    boxes = detect_objects(
        image,
        min_area=cfg.min_area
    )

    crops = crop_objects(
        image,
        boxes,
        padding=cfg.padding,
        size=cfg.output_size
    )

    save_crops(crops, cfg.output_path)

    if cfg.debug:
        ensure_dir(cfg.debug_path)
        save_debug_image(image, boxes, cfg.debug_path)