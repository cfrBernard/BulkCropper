import requests


def predict(cfg, image_path):

    with open(image_path, "rb") as f:

        res = requests.post(
            cfg.api_url,
            headers={
                "accept": "application/json"
            },
            files={
                "query_image": (
                    image_path.name,
                    f,
                    "image/png"
                )
            },
            timeout=30,
        )

    res.raise_for_status()

    return res.json()


def normalize_response(response):

    candidates = []

    items = response.get("items", [])

    for item in items:

        id_ = item.get("id")

        name = item.get("name")

        bricklink = None

        ext = item.get("external_sites", [])

        for e in ext:

            if e.get("name") == "BrickLink":

                bricklink = e.get("url")

                if bricklink and not bricklink.endswith("=P"):
                    bricklink += "=P"

        candidates.append(
            {
                "id": id_,
                "name": name,
                "bricklink": bricklink,
            }
        )

    return candidates