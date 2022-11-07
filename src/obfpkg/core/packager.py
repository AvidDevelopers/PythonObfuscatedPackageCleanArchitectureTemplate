import sys
from pathlib import Path
from os import listdir
import shutil
from subprocess import Popen, PIPE


class Package:
    def __init__(self, build_path: Path, output_path: Path, verbose: bool = False):
        self.build_path = build_path
        self.output_path = output_path
        self.verbose = verbose

    def build(self):
        process = Popen(
            [
                sys.executable,
                "setup.py",
                "bdist_wheel",
                "--dist-dir",
                "whl",
            ],
            cwd=f"{self.build_path}",
            stdout=PIPE,
            stderr=PIPE,
        )
        stdout, stderr = process.communicate()
        if self.verbose:
            print(stdout.decode("utf-8"), stderr.decode("utf-8"))

        if process.returncode == 0:
            package_filename = listdir(self.build_path / "whl")[0]
            print(f"###  Package `{package_filename}` file created successfully!")
        return stdout, stderr

    def move_to_output(self):
        files = listdir(self.build_path / "whl")
        for file in files:
            # Move and overwrite existing files
            shutil.move(
                str(self.build_path.joinpath(f"whl/{file}")),
                self.output_path.joinpath(f"{file}"),
            )
            print(f"###  Package `{file}` was moved to output!")
