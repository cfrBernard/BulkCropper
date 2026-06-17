import cv2


def detect_objects(mask, cfg, debug):

    count, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)

    boxes = []

    overlay = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    for i in range(1, count):

        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]

        if area < cfg.min_area:
            continue

        if cfg.remove_border_objects:

            if (
                x <= cfg.border_margin
                or y <= cfg.border_margin
                or x + w >= mask.shape[1] - cfg.border_margin
                or y + h >= mask.shape[0] - cfg.border_margin
            ):
                continue

        boxes.append(
            (
                x,
                y,
                w,
                h,
            )
        )

        cv2.rectangle(
            overlay,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2,
        )

    debug["08_boxes"] = overlay

    return boxes
