import cv2


def preprocess(image, cfg):

    debug = {}

    debug["original"] = image.copy()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    debug["gray"] = gray

    blur = cv2.GaussianBlur(
        gray,
        (cfg.gaussian_blur, cfg.gaussian_blur),
        0,
    )

    debug["blur"] = blur

    _, threshold = cv2.threshold(
        blur,
        cfg.background_threshold,
        255,
        cv2.THRESH_BINARY_INV,
    )

    debug["threshold"] = threshold

    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (cfg.morph_kernel, cfg.morph_kernel),
    )

    opened = cv2.morphologyEx(
        threshold,
        cv2.MORPH_OPEN,
        kernel,
        iterations=cfg.morph_iterations,
    )

    debug["open"] = opened

    closed = cv2.morphologyEx(
        opened,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=cfg.morph_iterations,
    )

    debug["final_mask"] = closed

    return closed, debug