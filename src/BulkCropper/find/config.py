from dataclasses import dataclass

@dataclass
class Config:

    # =========================
    # IO
    # =========================
    input_path: str = "data/output/<output_name>?"
    output_path: str = "data/output"
    debug_path: str = "var/debug"
    
    debug: bool = False