from typing import Union

from .cvrp import CVRP, parse_cvrp
from .utils import find_set
from .vrptw import VRPTW, parse_vrptw


def parse_instance(lines):
    """
    Parse the passed-in lines and return the corresponding instance.
    """
    # First line contains the name
    instance_name = lines[0].split(": ")[-1].strip()
    set_name = find_set(instance_name)

    if is_vrptw(set_name):
        instance = parse_vrptw(lines)
    else:
        instance = parse_cvrp(lines)

    return instance


def is_vrptw(set_name: str) -> bool:
    """
    Checks if the set name belons to VRPTW; otherwise it belons to CVRP.
    """
    return set_name in ["HG", "Solomon"]
