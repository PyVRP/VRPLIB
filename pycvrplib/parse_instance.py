from typing import List, Optional, Union

from .cvrp import CVRP, parse_cvrp
from .utils import find_set
from .vrptw import VRPTW, parse_vrptw


def parse_instance(lines):
    """
    Parse the passed-in lines and return the corresponding instance.
    """
    instance_name = parse_instance_name(lines)
    set_name = find_set(instance_name)

    instance: Union[VRPTW, CVRP]

    if is_vrptw(set_name):
        instance = parse_vrptw(lines)
    else:
        instance = parse_cvrp(lines)

    return instance


def parse_instance_name(lines: List[str]) -> str:
    # First line contains the name
    return lines[0].split(": ")[-1].strip()


def is_vrptw(set_name: str) -> bool:
    """
    Checks if the set name belons to VRPTW; otherwise it belons to CVRP.
    """
    return set_name in ["HG", "Solomon"]
