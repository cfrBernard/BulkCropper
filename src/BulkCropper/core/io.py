from pathlib import Path

import cv2


SUPPORTED = {
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".webp",
}


def load_images(cfg):

    root = Path(cfg.input_path)

    for file in sorted(root.iterdir()):

        if file.suffix.lower() not in SUPPORTED:
            continue

        image = cv2.imread(str(file))

        if image is None:
            continue

        yield file, image