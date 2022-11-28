from functools import lru_cache
from urllib.request import urlopen

from cvrplib.constants import CVRPLIB_URL
from cvrplib.read.parse_solution import parse_solution
from cvrplib.read.utils import find_set, strip_lines


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
    url = CVRPLIB_URL + f"{find_set(name)}/{name}.sol"
    response = urlopen(url).read().decode("utf-8")

    return parse_solution(strip_lines(response.split("\n")))
