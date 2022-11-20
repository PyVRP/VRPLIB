from .cvrp import parse_cvrp
from .utils import find_set
from .vrptw import parse_vrptw


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
    Checks if the set name belongs to VRPTW; otherwise it belons to CVRP.
    """
    # TODO This is not a foolproof way to differentiate between CVRP and VRPTW
    return set_name in ["HG", "Solomon"]
