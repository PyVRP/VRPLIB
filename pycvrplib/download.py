from functools import lru_cache

import requests

from ._parse_utils import parse_instance
from .constants import MEDIA_URL
from .solution import parse_solution


@lru_cache()
def download(name: str, solution: bool = False):
    """
    Download the instance from CVRPLIB directly. Also downloads the
    solution if solution=True.
    """
    response = requests.get(f"{MEDIA_URL}/{name}.vrp")

    if response.status_code == 404:
        raise ValueError(f"Invalid name: {name}")

    elif response.status_code != 200:
        response.raise_for_status()

    lines = response.text.splitlines()
    instance = parse_instance(lines)

    if solution:
        response_sol = requests.get(MEDIA_URL + name + ".sol")
        lines_sol = response_sol.text.splitlines()
        sol = parse_solution(lines_sol)
        return instance, sol

    return instance
