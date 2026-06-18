from pathlib import Path


def load_images(cfg):

    root = Path(cfg.output_root)

    jobs = []

    for folder in sorted(root.iterdir()):

        if not folder.is_dir():
            continue

        images = list(folder.glob("*.png"))

        if not images:
            continue

        for img in images:

            jobs.append(
                {
                    "folder": folder,
                    "image": img,
                    "json": folder / "brickognize.json",
                }
            )

    return jobs