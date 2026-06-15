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

    # ==========================
    # DEBUG OVERLAY
    # ==========================

    overlay = image.copy()

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

        cv2.imwrite(
            str(
                out_dir / f"ID_{idx+1:04d}.png"
            ),
            crop,
        )

        export_w = x2 - x1
        export_h = y2 - y1

        # ==========================
        # EXPORT AREA (padding)
        # ==========================

        cv2.rectangle(
            overlay,
            (x1, y1),
            (x2, y2),
            (255, 0, 0),
            2,
        )

        # ==========================
        # DETECTED BBOX
        # ==========================

        cv2.rectangle(
            overlay,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2,
        )

        # ==========================
        # PADDING GIZMO
        # ==========================

        cv2.line(
            overlay,
            (x1, y),
            (x, y),
            (0, 255, 255),
            1,
        )

        cv2.line(
            overlay,
            (x + w, y),
            (x2, y),
            (0, 255, 255),
            1,
        )

        cv2.line(
            overlay,
            (x, y1),
            (x, y),
            (0, 255, 255),
            1,
        )

        cv2.line(
            overlay,
            (x, y + h),
            (x, y2),
            (0, 255, 255),
            1,
        )

        # ==========================
        # INFO BOX
        # ==========================

        lines = [
            f"ID      : {idx+1}",
            f"BBox    : {w}x{h}",
            f"Padding : {padding}px",
            f"Export  : {export_w}x{export_h}",
        ]

        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.45
        thickness = 1

        line_height = 16
        box_width = 170
        box_height = len(lines) * line_height + 8

        tx = x
        ty = y - box_height - 5

        if ty < 5:
            ty = y + h + 5

        if tx + box_width > image.shape[1]:
            tx = image.shape[1] - box_width - 5

        if tx < 5:
            tx = 5

        # black bg
        cv2.rectangle(
            overlay,
            (tx, ty),
            (tx + box_width, ty + box_height),
            (0, 0, 0),
            -1,
        )

        # white border
        cv2.rectangle(
            overlay,
            (tx, ty),
            (tx + box_width, ty + box_height),
            (255, 255, 255),
            1,
        )

        # text
        for i, line in enumerate(lines):

            cv2.putText(
                overlay,
                line,
                (
                    tx + 5,
                    ty + 16 + i * line_height,
                ),
                font,
                scale,
                (255, 255, 255),
                thickness,
                cv2.LINE_AA,
            )

    debug["09_crop-infos"] = overlay

    save_debug(
        image_path.stem,
        debug,
        cfg,
    )