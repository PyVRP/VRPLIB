from functools import lru_cache

import requests

from .constants import MEDIA_URL
from .parse_instance import parse_instance
from .parse_solution import parse_solution
from .utils import find_set, is_vrptw, strip_lines


@lru_cache()
def download(name: str, solution: bool = False):
    """
    Download the instance from CVRPLIB directly. If `solution` is set, then
    also download the corresponding solution.
    """
    response = requests.get(f"{MEDIA_URL}/{_make_subpath(name)}")

    if response.status_code != 200:
        response.raise_for_status()

    instance = parse_instance(strip_lines(response.text.splitlines()))

    if not solution:
        return instance

    else:
        response_sol = requests.get(f"{MEDIA_URL}/{_make_subpath(name, True)}")

        if response_sol.status_code != 200:
            response_sol.raise_for_status()

        sol = parse_solution(strip_lines(response_sol.text.splitlines()))
        return instance, sol


def _make_subpath(name: str, solution: bool = False) -> str:
    """
    Return the path of the passed-in instance name relative to `MEDIA_URL`.
    """
    if solution:
        ext = "sol"
    else:
        ext = "txt" if is_vrptw(name) else "vrp"

    return f"{find_set(name)}/{name}.{ext}"
