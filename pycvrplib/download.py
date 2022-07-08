from functools import lru_cache

import requests

from .constants import MEDIA_URL
from .parse_instance import parse_instance
from .parse_solution import parse_solution
from .utils import find_set, is_vrptw


@lru_cache()
def download(name: str, solution: bool = False):
    """
    Download the instance from CVRPLIB directly. If `solution` is set, then
    also download the corresponding solution.
    """
    response = requests.get(f"{MEDIA_URL}/{_make_subpath(name)}")

    if response.status_code != 200:
        response.raise_for_status()

    instance = parse_instance(_read_nonempty_lines(response))

    if not solution:
        return instance

    else:
        response_sol = requests.get(f"{MEDIA_URL}/{_make_subpath(name, True)}")

        if response_sol.status_code != 200:
            response_sol.raise_for_status()

        sol = parse_solution(_read_nonempty_lines(response_sol))
        return instance, sol


def _make_subpath(name: str, solution: bool = False) -> str:
    """
    Return the path of the passed-in instance name relative to `MEDIA_URL`.
    """
    set_name = find_set(name)

    if solution:
        ext = "sol"
    else:
        ext = "txt" if is_vrptw(set_name) else "vrp"

    return f"{set_name}/{name}.{ext}"


def _read_nonempty_lines(response):
    return [l for l in (line.strip() for line in response.text.splitlines()) if l]
