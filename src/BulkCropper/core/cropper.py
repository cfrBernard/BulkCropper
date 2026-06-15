from pathlib import Path

import cv2
import numpy as np

from .debug import save_debug


def export_crops(
    image,
    image_path,
    boxes,
    mask,
    cfg,
    debug,
):

    out_dir = Path(cfg.output_path) / image_path.stem

    out_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    for idx, (x, y, w, h) in enumerate(boxes):

        padding = max(
            cfg.min_padding,
            int(max(w, h) * cfg.padding_ratio),
        )

        x1 = max(0, x - padding)
        y1 = max(0, y - padding)

        x2 = min(image.shape[1], x + w + padding)
        y2 = min(image.shape[0], y + h + padding)

        crop = image[y1:y2, x1:x2]

        crop_mask = mask[y1:y2, x1:x2]

        rgba = cv2.cvtColor(
            crop,
            cv2.COLOR_BGR2BGRA,
        )

        rgba[:, :, 3] = crop_mask

        cv2.imwrite(
            str(
                out_dir / f"piece_{idx+1:04d}.png"
            ),
            rgba,
        )

    save_debug(
        image_path.stem,
        debug,
        cfg,
    )
