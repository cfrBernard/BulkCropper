# Project Insight

## Design philosophy

BulkCropper focuses on simplicity.

Instead of relying on heavy AI models, the project uses classical computer vision techniques to achieve fast and deterministic results.

The objective is to provide a lightweight utility that can process hundreds or thousands of objects with minimal setup.

## Why LEGO?

The project is primarily optimized around LEGO because they provide an excellent benchmark for segmentation:

- many colors
- many shapes
- reflective plastic surfaces
- complex geometries

But, If the algorithm performs well on LEGO pieces, it generally performs well on many other isolated objects as well.

> And most importantly, it plans to host the Brickognize API. That's why I use it after all 😀.

---

## Brickognize API integration (v2)

The Brickognize module is fully decoupled from the cropping pipeline.

Reason:
- crop pipeline must remain deterministic and offline
- API calls introduce latency and failure points
- separation allows optional usage

---

## Structure

```
BulkCropper/
├── data/
│   ├── brickognize_cache.json
│   ├── input/
│   │   └── bulk.png
│   └── output/
│       └── bulk/
│           ├── brickognize.json
│           └── ID_0001.png
├── docs/
│   ├── CHANGELOG.md
│   ├── config-guide.md
│   ├── dev-insight.md
│   ├── integrations/
│   │   └── brickognize.md
│   └── roadmap.md
├── LICENSE.md
├── pyproject.toml
├── README.md
├── src/
│   ├── BulkCropper/
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── cli.py
│   │   ├── crop/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── cropper.py
│   │   │   ├── debug.py
│   │   │   ├── detector.py
│   │   │   ├── io.py
│   │   │   ├── pipeline.py
│   │   │   └── preprocessing.py
│   │   └── find/
│   │       ├── __init__.py
│   │       ├── api.py
│   │       ├── cache.py
│   │       ├── config.py
│   │       ├── io.py
│   │       └── pipeline.py
│   └── BulkCropperGUI/
│       ├── __init__.py
│       ├── __main__.py
│       ├── app.py
│       ├── controllers/
│       │   └── pipeline_controller.py
│       ├── services/
│       │   └── output_scanner.py
│       ├── widgets/
│       │   ├── details_panel.py
│       │   ├── explorer.py
│       │   ├── flow_layout.py
│       │   ├── image_card.py
│       │   └── sidebar.py
│       └── windows/
│           └── main_window.py
├── tests/
└── var/
    ├── cache/
    ├── debug/
    │   └── bulk/
    └── logs/
```

---

## Crop Processing pipeline

BulkCropper follows a deterministic computer vision pipeline:

```
Image 
│ 
▼ 
Preprocess 
│ 
▼ 
Mask Generation 
│ 
▼ 
Object Detection 
│ 
▼ 
Crop 
│ 
▼ 
PNG Export
```

> Each stage can be inspected through the debug system for easier tuning.

---

## API Processing pipeline

```
BulkCropper find
        │
        ▼
scan data/output/
        │
        ▼
for each folder
        │
        ├── AllImg.png
        │
        ▼
SHA256 image
        │
        ▼

cache ?
     │        │
    yes      no
     │        │
     │ Brickognize call
     │        │
     └────────┘
              │
              ▼
      normalized result
              │
              ▼
      brickognize.json
```

---
