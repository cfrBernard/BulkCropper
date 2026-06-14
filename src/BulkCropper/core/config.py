from dataclasses import dataclass


@dataclass
class Config:
    # --- IO ---
    input_path: str = "data/input"
    output_path: str = "data/output"

    # --- detection ---
    min_area: int = 400

    # --- crop ---
    padding: int = 20
    output_size: int = 512

    # --- background ---
    background: str = "white"  # "white" | "transparent"

    # --- debug ---
    debug: bool = False
    debug_path: str = "var/debug"

    # --- behavior ---
    save_debug_overlay: bool = True