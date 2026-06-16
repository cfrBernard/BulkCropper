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

## Structure

```
BulkCropper/
├── data/
│   ├── input/
│   │   └── bulk.png
│   └── output/
│       └── bulk/
├── docs/
├── pyproject.toml
├── README.md
├── src/
│   └── BulkCropper/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   ├── cropper.py
│       │   ├── debug.py
│       │   ├── detector.py
│       │   ├── io.py
│       │   ├── preprocessing.py
│       │   └── utils.py
│       └── pipeline.py
├── tests/
└── var/
    ├── cache/
    ├── debug/
    │   └── bulk/
    └── logs/
```

---

## Processing pipeline

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
