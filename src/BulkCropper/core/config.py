from dataclasses import dataclass

@dataclass
class Config:

    input_path = "data/input"
    output_path = "data/output"
    debug_path = "var/debug"

    debug = True

    output_size = 512

    background_threshold = 245

    gaussian_blur = 5

    morph_kernel = 3

    morph_iterations = 2

    padding_ratio = 0.08

    min_padding = 10

    min_area = 300

    border_margin = 4

    remove_border_objects = True
 
    # square_output = True
    # 
    # transparent_png = True
    # 
    # adaptive = False
    # 
    # adaptive_blocksize = 31
    # 
    # adaptive_c = 8