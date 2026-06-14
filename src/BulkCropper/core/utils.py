import cv2
import os


def load_image(path):
    return cv2.imread(path)


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def save_crops(crops, output_path):
    ensure_dir(output_path)

    for i, crop in enumerate(crops):
        cv2.imwrite(
            os.path.join(output_path, f"{i:04d}.png"),
            crop
        )


def save_debug_image(image, boxes, debug_path):
    img = image.copy()

    for i, (x, y, w, h) in enumerate(boxes):
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(
            img,
            str(i),
            (x, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1
        )

    cv2.imwrite(os.path.join(debug_path, "debug.png"), img)