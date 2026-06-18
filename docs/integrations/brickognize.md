# Brickognize Integration (v2)

BulkCropper v2 introduces an optional integration with the **Brickognize API**, allowing automatic identification of detected objects after the cropping pipeline.

This feature is completely decoupled from the core cropping system and is designed as an **optional post-processing step**.

> ⚠️ Brickognize is a public API with unknown rate limits. Use with caution on large datasets.

---

## How it works

The integration operates as a separate pipeline:

1. BulkCropper processes images using the core cropping system
2. Cropped images are saved in `data/output/<folder_name>/`
3. The Brickognize module scans these `.png` files
4. Each image is sent to the Brickognize API
5. Results are aggregated per folder
6. A JSON file is generated inside the same output folder

---

## Usage

The feature is executed via the CLI:

```bash
BulkCropper find
```

### Requirements

- Input images must already be processed by the cropper
- Only .png files are currently supported
- Images must exist inside `data/output/<folder_name>/`

--- 

## Output format

For each processed folder, BulkCropper generates a JSON file in the same directory.

Example structure:

```json
[
    {
        "folder": "bulk",
        "input_id": "ID_0001.png",
        "status": "NOT_FOUND",
        "items": "not found"
    },
    {
        "folder": "bulk",
        "input_id": "ID_0002.png",
        "status": "OK",
        "items": [
            {
                "id": "970c00pb0747",
                "name": "Hips and Legs with Cargo Pockets with Flaps and Pleats Pattern",
                "bricklink": "https://www.bricklink.com/v2/catalog/catalogitem.page?P=970c00pb0747"
            }
        ]
    },
    {
        "folder": "bulk",
        "input_id": "ID_0003.png",
        "status": "OK",
        "items": [
            {
                "id": "3626pb1544",
                "name": "Minifigure, Head Alien with Wrestler Mask with Large Dark Red Eyes, Lime Hose on Back Pattern (Bane)",
                "bricklink": "https://www.bricklink.com/v2/catalog/catalogitem.page?P=3626pb1544"
            },
            {
                "id": "3626pb2110",
                "name": "Minifigure, Head Dual Sided Alien Female with Red Eyes, Lavender Lower Face, Smiling / Scowling Expression Pattern",
                "bricklink": "https://www.bricklink.com/v2/catalog/catalogitem.page?P=3626pb2110"
            }
        ]
    }
]
```

## Caching system

To reduce redundant API calls, the integration uses a local cache file:

```
data/brickognize_cache.json
```

> This cache stores previous API responses and is automatically reused when possible.

---

## Rate limiting & performance

Brickognize does not provide explicit rate limit documentation.

To prevent potential blocking or overload:

- A configurable delay is applied between requests
- This can be adjusted in `src/BulkCropper/find/config.py`

### Recommendation

- Keep delays enabled for large datasets
- Avoid running the tool on very large inventories without testing
- Expect variability in response times

---

## Limitations

- No guaranteed API rate limits
- No official SLA or performance guarantees
- Only .png inputs are supported for now
- Not tested on large-scale inventories
- Results may vary depending on image quality

---

## Design notes

This module is intentionally separated from the core cropping pipeline:

- The cropper remains fully offline and deterministic
- The Brickognize integration acts as an optional enrichment layer
- Failures in the API do not affect cropping output

--- 

## Output location summary

For each processed folder:

- Input: `data/output/<folder_name>/*.png`
- Output: `data/output/<folder_name>/*.json`
- Cache: `data/brickognize_cache.json`

---

## Safety note

This feature relies on an external public API.

> Performance, availability, and correctness are outside of BulkCropper's control.

---
