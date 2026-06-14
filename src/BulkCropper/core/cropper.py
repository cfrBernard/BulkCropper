import cv2
import numpy as np


def crop_objects(image, boxes, padding=20, size=512):
    crops = []

    h_img, w_img = image.shape[:2]

    for (x, y, w, h) in boxes:

        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(w_img, x + w + padding)
        y2 = min(h_img, y + h + padding)

        crop = image[y1:y2, x1:x2]

        crop = make_square(crop, size)

        crops.append(crop)

    return crops


def make_square(img, size):
    h, w = img.shape[:2]

    max_side = max(h, w)

    canvas = np.ones((max_side, max_side, 3), dtype=np.uint8) * 255

    y_offset = (max_side - h) // 2
    x_offset = (max_side - w) // 2

    canvas[y_offset:y_offset+h, x_offset:x_offset+w] = img

    return cv2.resize(canvas, (size, size))