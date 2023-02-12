from urllib.request import urlopen

from .constants import CVRPLIB_URL
from .download_utils import find_set, is_vrptw


def download_instance(name: str, path: str):
    """
    Downloads an instance file from CVRPLIB and saves it at the specified path.

    Parameters
    ----------
    name
        The name of the instance to download. Should be one of the names
        listed in `vrplib.list_instances()`.
    path
        The path where the instance file should be saved.
    """
    ext = "txt" if is_vrptw(name) else "vrp"
    url = CVRPLIB_URL + f"{find_set(name)}/{name}.{ext}"
    response = urlopen(url, timeout=30)

    instance_text = response.read().decode("utf-8")

    with open(path, "w") as fi:
        fi.write(instance_text)
