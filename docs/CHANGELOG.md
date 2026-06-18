# Changelog

## [v2.0.0] – 2026-06-18

#### **Optional Brickognize API integration**

### Added

- Brickognize API integration module
- new `find/` pipeline
- optional LEGO part identification step after cropping
- New CLI : `BulkCropper crop` & `BulkCropper find`

---

## [v1.1.1] – 2026-06-17

### Fixes

* Docs / version fixes

---

## [v1.1.0] – 2026-06-17

#### **Structure setup for the future API system**

### Added

* Separation of systems
* New find folder (src/BulkCropper/find/)
* Core folder rename (src/BulkCropper/crop/)
* Each will have their own pipeline / config
* Same CLI for both systems (parser / args)

---

## [v1.0.0] – 2026-06-16

#### **Initial Public Release**

### Added

* Batch processing of multiple images
* Automatic object detection and segmentation
* Individual PNG export
* Support for PNG, JPG, JPEG, BMP and WEBP inputs
* Configurable processing pipeline
* Complete debug image generation system
* Padding-aware crop export
* Border object filtering
* Lightweight implementation based only on OpenCV and NumPy

---

## [v0.3.0] – 2026-06-16

### Added

* New saturation debug image (`02_saturation`)
* Crop visualization debug image with detailed export information
* Bounding box overlay
* Export area visualization
* Padding gizmo visualization
* Object ID display
* Bounding box size display
* Applied padding information
* Final exported image size information

### Improved

* Significantly improved debugging experience
* Easier parameter tuning through visual feedback

---

## [v0.2.2] – 2026-06-15

### Changed

* Removed mask-based crop generation
* Simplified the export pipeline

---

## [v0.2.1] – 2026-06-15

### Added

* Edge detection pipeline based on Canny
* Edge dilation stage
* Contour filling system
* Improved object reconstruction for difficult shapes

---

## [v0.2.0] – 2026-06-15

### Changed

* Switched preprocessing from grayscale analysis to HSV saturation segmentation

### Improved

* Better separation between colorful objects and white backgrounds
* More robust color-based segmentation

---

## [v0.1.0] – 2026-06-15

### Added

* First complete processing pipeline
* Initial project architecture
* Image preprocessing
* Object detection
* Crop generation
* PNG export system

### Changed

* Major internal refactor establishing the project's final architecture

---

## [v0.0.1] – 2026-06-14

### Added

* Initial project setup
* Base repository structure
* First implementation prototype
