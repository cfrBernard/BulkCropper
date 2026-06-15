import cv2
import numpy as np


def preprocess(image, cfg):

    debug = {}
    debug["original"] = image.copy()

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(hsv)

    debug["saturation"] = s
    debug["value"] = v

    # MAIN MASK (LEGO = colors)
    mask = (s > cfg.saturation_threshold).astype(np.uint8) * 255

    debug["mask_raw"] = mask

    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (cfg.morph_kernel, cfg.morph_kernel),
    )

    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=cfg.morph_iterations)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=cfg.morph_iterations)

    debug["final_mask"] = mask

    return mask, debug