import argparse

from .crop.pipeline import run_pipeline as run_crop
from .find.pipeline import run_pipeline as run_find


def main():

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser("crop")
    subparsers.add_parser("find")

    args = parser.parse_args()

    if args.command == "crop":
        run_crop(args)

    elif args.command == "find":
        run_find(args)