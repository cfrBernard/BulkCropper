from pathlib import Path

from .config import Config
from .io import load_images

def run_pipeline(args):

    cfg = Config()

    images = load_images(cfg)