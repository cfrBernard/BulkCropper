import argparse
from .pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)

    parser.add_argument("--debug", action="store_true")

    parser.add_argument("--padding", type=int, default=20)
    parser.add_argument("--min-area", type=int, default=400)
    parser.add_argument("--size", type=int, default=512)

    args = parser.parse_args()

    run_pipeline(
        input_path=args.input,
        output_path=args.output,
        debug=args.debug,
        padding=args.padding,
        min_area=args.min_area,
        size=args.size,
    )