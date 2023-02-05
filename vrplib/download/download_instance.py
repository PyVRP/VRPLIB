from functools import lru_cache
from urllib.request import urlopen

from vrplib.constants import CVRPLIB_URL
from vrplib.parse import parse_solomon, parse_vrplib

from .download_utils import find_set, is_vrptw


@lru_cache()
def download_instance(name: str):
    """
    Downloads an instance from CVRPLIB.

    Parameters
    ----------
    name
        The instance name. See `vrplib.list_instances` for all eligible names.

    Returns
    -------
    A dictionary that contains the instance data.
    """
    ext = "txt" if is_vrptw(name) else "vrp"
    response = urlopen(CVRPLIB_URL + f"{find_set(name)}/{name}.{ext}")

    parser = parse_solomon if is_vrptw(name) else parse_vrplib
    return parser(response.read().decode("utf-8"))
