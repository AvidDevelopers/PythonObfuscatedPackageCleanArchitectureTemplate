import argparse
from os import PathLike, path, mkdir
from pathlib import Path
from typing import Any, Dict, Union
import tempfile

from stubs import StubsGenerator
from pkg import PackageGenerator
from obfs import ObfusGenerator

try:
    from .utils import PathType, PathCheck, Exist
except ImportError:
    from utils import PathType, PathCheck, Exist  # type: ignore


STUBS_PACKAGE_DIR_NAME = "stubs-pkg"
MANIFEST_FILE_NAME = "MANIFEST.in"


def get_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="obfpkg",
        description="Obfuscate the python package and related tools",
        epilog="It can generate stubs package for development",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
    )
    parser.add_argument(
        "-s",
        "--src",
        metavar="src_pkg_dir",
        type=PathCheck(exists=Exist(check=True), ptype=PathType.DIR),
        help="The directory where the source package contained.",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        metavar="output_pkg_dir",
        type=PathCheck(exists=Exist(empty_or_not_exist=True), ptype=PathType.DIR),
        help="The directory where the obfuscated (and stubs) package will stored. default is: <src>/../dist ",
    )
    parser.add_argument(
        "-t",
        "--stubs-dir",
        metavar="stubs_pkg_dir",
        type=PathCheck(exists=Exist(check=True), ptype=PathType.DIR),
        help=f"The directory of stubs package project (needed 'setup.py' for build pkg-stubs). default is: <src>/../{STUBS_PACKAGE_DIR_NAME}",
    )

    return parser


def get_package_name(src: Path):
    all_package = [
        x for x in src.iterdir() if all([x.is_dir(), not x.name.startswith(".")])
    ]
    if len(all_package) > 1:
        # select package directory
        pass
    elif len(all_package) == 0:
        raise ValueError(f"Package not found in the {src}")
    else:
        package = all_package[0].name
    return package


def rewriter(path):
    lines = [
        "\nglobal-include  *.pyi",  # important for stubs package",
        "\nrecursive-include */pytransform *",  # important for obfuscate package",
    ]
    must_write_lines = []
    try:
        with open(path, "r") as f:
            content = f.read()
            for line in lines:
                if line.strip() not in content:
                    must_write_lines.append(line)
    except FileNotFoundError:
        must_write_lines = lines

    if must_write_lines:
        with open(path, "a") as f:
            f.writelines(must_write_lines)


def recreate_manifest(src: Path, stubs_pkg_dir: Union[PathLike, str]):
    rewriter(path.join(src, MANIFEST_FILE_NAME))
    rewriter(path.join(src.parent / stubs_pkg_dir, MANIFEST_FILE_NAME))


def create_stubs_package(src: Path, build_path: Path, output_dir: Path, package_name: str):
    stubs_generator = StubsGenerator(
        src=src,
        build_path=build_path,
        package_name=package_name,
    )
    stubs_generator.generate()

    # Start Build Package
    package_generator = PackageGenerator(
        src=build_path,
        destination=output_dir,
    )
    package_generator.generate()
    package_generator.move_to_output()

    stubs_generator.clean_up()


def create_obfuscated_package(src: Path, output_dir: Path, package_name: str):
    with tempfile.TemporaryDirectory(prefix="obf-pkg-", dir=src.parent) as tempdir:
        print("Start Process in:", tempdir)

        obf_pkg = ObfusGenerator(src, Path(tempdir), package_name)
        obf_pkg.generate()

        # Start Build Package
        package_generator = PackageGenerator(
            src=Path(tempdir).joinpath("dist"),
            destination=output_dir,
        )
        package_generator.generate()
        package_generator.move_to_output()


def main():
    args = get_args().parse_args()
    print(args)
    package_name = get_package_name(args.src)
    recreate_manifest(args.src, STUBS_PACKAGE_DIR_NAME)

    if args.output_dir is None:
        args.output_dir = args.src / f"../dist"
    try:
        mkdir(args.output_dir)
    except FileExistsError:
        pass

    build_path = (
        args.src / f"../{STUBS_PACKAGE_DIR_NAME}"
        if args.stubs_dir is None
        else args.stubs_dir
    )
    PathCheck(exists=Exist(check=True), ptype=PathType.DIR)(build_path)
    create_stubs_package(
        src=args.src,
        build_path=build_path,
        output_dir=args.output_dir,
        package_name=package_name,
    )

    create_obfuscated_package(
        src=args.src, output_dir=args.output_dir, package_name=package_name
    )


if __name__ == "__main__":
    main()
