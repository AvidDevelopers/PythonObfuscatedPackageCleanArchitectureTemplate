from os import rename, listdir
from pathlib import Path
from subprocess import Popen, PIPE
import shutil

STUBS_PACKAGE_DIR_NAME = "stubs-pkg"


class Stubs:
    """Generate the stubs project files from the source project."""

    def __init__(
        self, src_path: Path, build_path: Path, package_name: str, verbose: bool = False
    ):
        self.src_path = src_path
        self.build_path = build_path.resolve()
        self.package_name = package_name
        self.verbose = verbose

        self.clean_up()

    def _rename(self):
        for i in range(3, 0, -1):
            try:
                rename(
                    self.build_path / self.package_name,
                    self.build_path / f"{self.package_name}-stubs",
                )
                print("###  The stubs project generated successfully!")
                break
            except FileExistsError as ex:
                print(f"Error while renaming: {ex}")
                print(f"try to remove exist path... {i}")
                shutil.rmtree(
                    self.build_path / f"{self.package_name}-stubs",
                    ignore_errors=True,
                )
            except Exception as ex:
                print(f"Error while renaming: {ex}")
                print(f"Retrying... {i}")

    def generate(self):
        process = Popen(
            [
                "stubgen",
                "-o",
                self.build_path,
                "-p",
                f"{self.package_name}",
            ],
            cwd=f"{self.src_path}",
            stdout=PIPE,
            stderr=PIPE,
        )
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise Exception(
                f"Error while generating stubs: {stderr.decode('utf-8')}\n\nSTDOUT:\n{stdout.decode('utf-8')}"
            )
        else:
            self._rename()

        return stdout, stderr

    def overwrite_stubs_from_src(self):
        raise NotImplementedError

    def clean_up(self):
        build_abspath = self.build_path.resolve().absolute()
        dirs = {
            build_abspath / x
            for x in listdir(build_abspath)
            if (build_abspath / x).is_dir()
        }

        for x in dirs:
            shutil.rmtree(x)
