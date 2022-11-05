import argparse
from .utils import PathType, PathCheck, Exist


def get_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="obfpkg",
        description="Obfuscate the python package and related tools",
        epilog="It can generate stubs package for development",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument(
        "-s",
        "--src",
        type=PathCheck(exists=Exist(check=True), ptype=PathType.DIR),
        help='The directory where the source package contained.'
    )
    parser.add_argument(
        "-o",
        "--obf",
        type=PathCheck(exists=Exist(empty_or_not_exist=True), ptype=PathType.DIR),
        help='The directory where the obfuscated package will stored.'
    )

    return parser


def main():
    args = get_args().parse_args()
    print(args)


if __name__ == "__main__":
    main()
