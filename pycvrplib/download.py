from functools import lru_cache
from typing import Union

import requests

from ._parse_utils import Instance, parse_instance
from .constants import MEDIA_URL
from .solution import parse_solution
from .utils import find_set, parse_instance_name
from .vrptw import VRPTW, parse_vrptw


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

    instance_name = parse_instance_name(lines)
    set_name = find_set(instance_name)

    instance: Union[VRPTW, Instance]

    if set_name in ["Solomon", "HG"]:
        instance = parse_vrptw(lines)
    else:
        instance = parse_instance(lines)

    if solution:
        response_sol = requests.get(MEDIA_URL + name + ".sol")
        lines_sol = response_sol.text.splitlines()
        sol = parse_solution(lines_sol)
        return instance, sol

    return instance
