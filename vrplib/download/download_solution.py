from functools import lru_cache
from urllib.request import urlopen

from .constants import CVRPLIB_URL
from .download_utils import find_set


@lru_cache()
def download_solution(name: str, path: str):
    """
    Downloads a solution file from CVRPLIB and saves it at the specified path.

    Parameters
    ----------
    name
        The name of the instance to download. Should be one of the names
        listed in `vrplib.list_instances`.
    path
        The path where the solution file should be saved.
    """
    response = urlopen(CVRPLIB_URL + f"{find_set(name)}/{name}.sol")
    solution_text = response.read().decode("utf-8")

    with open(path, "w") as fi:
        fi.write(solution_text)
