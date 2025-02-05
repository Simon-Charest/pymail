from os.path import exists
from pathlib import Path
from shutil import rmtree


def delete(path: Path) -> None:
    if exists(path):
        rmtree(path)
