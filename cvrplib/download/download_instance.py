from functools import lru_cache

import requests

from cvrplib.constants import CVRPLIB_URL
from cvrplib.read.parse_solomon import parse_solomon
from cvrplib.read.parse_vrplib import parse_vrplib
from cvrplib.read.utils import find_set, is_vrptw, strip_lines


# TODO Change here to IOStream
@lru_cache()
def download_instance(name: str):
    """
    Downloads an instance from CVRPLIB.

    Parameters
    ----------
    name
        The instance name. See `cvrplib.list_instances` for all eligible names.

    Returns
    -------
    A dictionary that contains the instance data.

    """
    ext = "txt" if is_vrptw(name) else "vrp"
    response = requests.get(CVRPLIB_URL + f"{find_set(name)}/{name}.{ext}")

    if response.status_code != 200:
        response.raise_for_status()

    parser = parse_solomon if is_vrptw(name) else parse_vrplib
    return parser(strip_lines(response.text.splitlines()))
