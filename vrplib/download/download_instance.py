import os
from pathlib import Path
from typing import Union
from urllib.request import urlopen

from .constants import CVRPLIB_URL
from .download_utils import find_set, is_vrptw


def download_instance(name: str, path: Union[str, os.PathLike]):
    """
    Downloads an instance file from CVRPLIB and saves it at the specified path.

    Parameters
    ----------
    name
        The name of the instance to download. Should be one of the names
        listed in `vrplib.list_instances()`.
    path
        The path where the instance file should be saved. If a directory is
        specified, the file will be saved in that directory with the original
        file name.
    """
    ext = "txt" if is_vrptw(name) else "vrp"
    url = CVRPLIB_URL + f"{find_set(name)}/{name}.{ext}"
    response = urlopen(url, timeout=30)

    instance_text = response.read().decode("utf-8")

    if os.path.isdir(path):
        path = Path(path) / f"{name}.{ext}"

    with open(path, "w") as fi:
        fi.write(instance_text)
