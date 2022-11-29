from functools import lru_cache
from urllib.request import urlopen

from cvrplib.constants import CVRPLIB_URL
from cvrplib.parse import parse_solution

from .download_utils import find_set


@lru_cache()
def download_solution(name: str):
    """
    Downloads a solution from CVRPLIB.

    Parameters
    ----------
    name
        The instance name. See `cvrplib.list_instances` for all eligible names.

    Returns
    -------
    A dictionary containing the solution data.
    """
    response = urlopen(CVRPLIB_URL + f"{find_set(name)}/{name}.sol")

    return parse_solution(response.read().decode("utf-8"))
