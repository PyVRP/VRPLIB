from functools import lru_cache

import requests

from cvrplib.constants import CVRPLIB_URL
from cvrplib.read.parse_solomon import parse_solomon
from cvrplib.read.parse_vrplib import parse_vrplib
from cvrplib.read.utils import find_set, is_vrptw, strip_lines


@lru_cache()
def download_instance(name: str):
    """
    Download a instance from CVRPLIB.

    Params
    ------
    name
        The instance name. See `cvrp.list_instances` for all eligible names.

    """
    ext = "txt" if is_vrptw(name) else "vrp"
    response = requests.get(CVRPLIB_URL + f"{find_set(name)}/{name}.{ext}")

    if response.status_code != 200:
        response.raise_for_status()

    lines = strip_lines(response.text.splitlines())

    if is_vrptw(name):
        return parse_solomon(lines)
    else:
        return parse_vrplib(lines)
