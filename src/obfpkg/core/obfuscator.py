from typing import List, Tuple
from os import listdir
import time
from subprocess import Popen, PIPE
from pathlib import Path
import shutil

obf_cmds = [
    "pyarmor init --src {src_pkg} --entry __init__.py config",
    "pyarmor build --platform windows.x86_64 --platform linux.x86_64 --platform darwin.x86_64 --output dist --only-runtime config",
    "pyarmor build --output dist --no-runtime config",
]


def formate_split(cmd: str, **kwargs):
    parts = [part.format(**kwargs) for part in cmd.split()]
    return parts


class Obfuscate:
    def __init__(
        self,
        src_path: Path,
        obf_build_path: Path,
        package_name: str,
        verbose: bool = False,
    ):
        self.src = src_path
        self.obf_build_path = obf_build_path
        self.package_name = package_name
        self.verbose = verbose

        self.obf_pkg_path = obf_build_path / "dist"

    def correct_path(self):
        package_init_path = self.obf_pkg_path / self.package_name / "__init__.py"
        with open(package_init_path) as init:
            lines = init.readlines()
            lines.pop(0)
            lines.insert(0, "from .pytransform import pyarmor_runtime\n")

        with open(package_init_path, "w") as init:
            init.writelines(lines)

    def relocate_pytransform(self):
        pytransform_path = self.obf_pkg_path / "pytransform"
        res = shutil.move(
            f"{pytransform_path}", f"{self.obf_pkg_path / self.package_name}"
        )
        if res:
            self.correct_path()

    def build(self):
        processes: List[Popen] = []
        results: List[Tuple[bytes, bytes]] = []
        for cmd in obf_cmds:
            processes.append(
                Popen(
                    formate_split(
                        cmd,
                        src_pkg=self.src.absolute().joinpath(self.package_name),
                    ),
                    cwd=f"{self.obf_build_path}",
                    stdout=PIPE,
                    stderr=PIPE,
                )
            )
            results.append(processes[-1].communicate())
            time.sleep(0.5)

        if self.verbose:
            for out, err in results:
                print(out.decode("utf-8"))
                print(err.decode("utf-8"))

        if all([p.returncode == 0 for p in processes]):
            self.relocate_pytransform()
            self.copy_setup_files_from_src()
            print(f"###  The obfuscate project generated successfully!")

        return results

    def copy_setup_files_from_src(self):
        for file in ["setup.py", "MANIFEST.in"]:
            shutil.copy(
                self.src / file,
                self.obf_pkg_path,
            )
