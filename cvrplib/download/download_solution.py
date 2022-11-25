from functools import lru_cache

import requests

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
    response = requests.get(CVRPLIB_URL + f"{find_set(name)}/{name}.sol")

    if response.status_code != 200:
        response.raise_for_status()

    return parse_solution(strip_lines(response.text.splitlines()))
