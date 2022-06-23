from functools import lru_cache
from typing import Union

import requests

from .constants import MEDIA_URL
from .cvrp import CVRP, parse_cvrp
from .parse_instance import parse_instance
from .parse_solution import parse_solution
from .utils import find_set, is_vrptw
from .vrptw import VRPTW, parse_vrptw


@lru_cache()
def download(name: str, solution: bool = False):
    """
    Download the instance from CVRPLIB directly. Also downloads the
    solution if solution=True.
    """
    set_name = find_set(name)
    ext = "txt" if set_name in ["Solomon", "HG"] else "vrp"
    response = requests.get(f"{MEDIA_URL}/{set_name}/{name}.{ext}")

    if response.status_code == 404:
        raise ValueError(f"Unknown instance name: {name}")

    elif response.status_code != 200:
        response.raise_for_status()

    lines = [line for line in response.text.splitlines() if line.strip()]

    instance = parse_instance(lines)

    if solution:
        response_sol = requests.get(f"{MEDIA_URL}/{set_name}/{name}.sol")
        lines_sol = response_sol.text.splitlines()
        sol = parse_solution(lines_sol)
        return instance, sol

    return instance
