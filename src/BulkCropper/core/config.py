from dataclasses import dataclass

@dataclass
class Config:

    # =========================
    # IO
    # =========================
    input_path: str = "data/input"
    output_path: str = "data/output"
    debug_path: str = "var/debug"
    
    debug: bool = True

    # =========================
    # GENERAL
    # =========================
    output_size: int = 512

    # =========================
    # SEGMENTATION COLOR
    # =========================
    saturation_threshold: int = 40

    # =========================
    # EDGE SYSTEM
    # =========================
    canny_low: int = 40
    canny_high: int = 120

    edge_kernel_size: int = 3
    edge_dilate_iterations: int = 2

    gaussian_blur = 5

    # =========================
    # MORPHOLOGY
    # =========================
    morph_kernel: int = 3
    morph_iterations: int = 2

    # =========================
    # FILTERING
    # =========================
    min_area: int = 300
    max_area: int = 10_000_000

    border_margin: int = 4
    remove_border_objects: bool = True

    # =========================
    # CROP
    # =========================
    padding_ratio: float = 0.08
    min_padding: int = 10
