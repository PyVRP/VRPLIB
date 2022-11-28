from functools import lru_cache
from urllib.request import urlopen

from cvrplib.constants import CVRPLIB_URL
from cvrplib.read.parse_solomon import parse_solomon
from cvrplib.read.parse_vrplib import parse_vrplib
from cvrplib.read.utils import strip_lines

from .download_utils import find_set, is_vrptw


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
    url = CVRPLIB_URL + f"{find_set(name)}/{name}.{ext}"
    response = urlopen(url).read().decode("utf-8")

    parser = parse_solomon if is_vrptw(name) else parse_vrplib

    return parser(strip_lines(response.split("\n")))
