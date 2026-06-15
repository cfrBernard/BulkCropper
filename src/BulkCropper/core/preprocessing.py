import cv2
import numpy as np


def preprocess(image, cfg):

    debug = {}
    debug["00_original"] = image.copy()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    debug["01_gray"] = gray

    # =========================
    # MASK COLOR
    # =========================
    mask_color = (s > cfg.saturation_threshold).astype(np.uint8) * 255
    debug["02_mask_color"] = mask_color

    # =========================
    # EDGES
    # =========================
    blur = cv2.GaussianBlur(
        gray,
        (cfg.gaussian_blur, cfg.gaussian_blur),
        0
    )

    edges = cv2.Canny(gray, cfg.canny_low, cfg.canny_high)
    debug["03_edges"] = edges

    # =========================
    # EDGE DILATION
    # =========================
    kernel_edge = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (cfg.edge_kernel_size, cfg.edge_kernel_size)
    )

    edges_dilated = cv2.dilate(
        edges,
        kernel_edge,
        iterations=cfg.edge_dilate_iterations
    )

    debug["04_edges_dilated"] = edges_dilated

    # =========================
    # FILL CONTOURS
    # =========================
    contours, _ = cv2.findContours(
        edges_dilated,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    filled = np.zeros_like(gray)
    cv2.drawContours(filled, contours, -1, 255, thickness=cv2.FILLED)

    debug["05_filled"] = filled

    # =========================
    # COMBINATION
    # =========================
    mask = cv2.bitwise_or(mask_color, filled)
    debug["06_combined"] = mask

    # =========================
    # CLEANING
    # =========================
    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (cfg.morph_kernel, cfg.morph_kernel)
    )

    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=cfg.morph_iterations)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=cfg.morph_iterations)

    debug["08_final"] = mask

    return mask, debug
