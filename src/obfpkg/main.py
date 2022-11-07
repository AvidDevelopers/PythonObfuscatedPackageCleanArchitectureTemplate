import argparse
from os import mkdir
from pathlib import Path
import tempfile

try:
    # package style import
    from .core import Package, Stubs, Obfuscate
    from .utils import PathType, PathCheck, Exist
except ImportError:
    # project style import
    from core import Package, Stubs, Obfuscate  # type: ignore
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


def rewriter(path: Path):
    lines = [
        "\nglobal-include  *.pyi",  # important for stubs package",
        "\nrecursive-include */pytransform *",  # important for obfuscate package",
    ]
    must_write_lines = []
    try:
        with open(path.resolve(), "r") as f:
            content = f.read()
            for line in lines:
                if line.strip() not in content:
                    must_write_lines.append(line)
    except FileNotFoundError:
        must_write_lines = lines

    if must_write_lines:
        with open(path, "a") as f:
            f.writelines(must_write_lines)


def recreate_manifest(src: Path, stubs_build_path: Path):
    for path in [src, stubs_build_path]:
        rewriter(path.joinpath(MANIFEST_FILE_NAME))


def create_stubs_package(
    src: Path,
    build_path: Path,
    output_dir: Path,
    package_name: str,
    verbose: bool = False,
):
    stubs_generator = Stubs(
        src_path=src,
        build_path=build_path,
        package_name=package_name,
        verbose=verbose,
    )
    stubs_generator.generate()

    # Start Build Package
    package_generator = Package(
        build_path=build_path,
        output_path=output_dir,
        verbose=verbose,
    )
    package_generator.build()
    package_generator.move_to_output()

    stubs_generator.clean_up()


def create_obfuscated_package(
    src: Path, output_dir: Path, package_name: str, verbose: bool = False
):
    with tempfile.TemporaryDirectory(prefix="obf-pkg-", dir=src.parent) as tempdir:
        print("###  Start Process in:", tempdir)

        obf_pkg = Obfuscate(src, Path(tempdir), package_name, verbose=verbose)
        obf_pkg.build()

        # Start Build Package
        package_generator = Package(
            build_path=Path(tempdir).joinpath("dist"),
            output_path=output_dir,
            verbose=verbose,
        )
        package_generator.build()
        package_generator.move_to_output()


def main():
    args = get_args().parse_args()
    package_name = get_package_name(args.src)

    for k, v in vars(args).items():
        print(f"{k:>15}: {v!r:<20}")
    print()

    stubs_build_path = (
        args.src / f"../{STUBS_PACKAGE_DIR_NAME}"
        if args.stubs_dir is None
        else args.stubs_dir
    )
    if args.output_dir is None:
        args.output_dir = (args.src / f"../dist").resolve()
    try:
        mkdir(args.output_dir)
    except FileExistsError:
        pass

    recreate_manifest(args.src, stubs_build_path)

    PathCheck(exists=Exist(check=True), ptype=PathType.DIR)(stubs_build_path)
    create_stubs_package(
        src=args.src,
        build_path=stubs_build_path,
        output_dir=args.output_dir,
        package_name=package_name,
        verbose=args.verbose,
    )

    create_obfuscated_package(
        src=args.src,
        output_dir=args.output_dir,
        package_name=package_name,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
