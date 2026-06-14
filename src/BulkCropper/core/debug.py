from pathlib import Path

import cv2


def save_debug(name, debug, cfg):

    if not cfg.debug:
        return

    root = Path(cfg.debug_path) / name

    root.mkdir(
        parents=True,
        exist_ok=True,
    )

    for key, img in debug.items():

        cv2.imwrite(
            str(root / f"{key}.png"),
            img,
        )