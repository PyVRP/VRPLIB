from typing import List, Optional, Union

from .cvrp import Instance, parse_cvrp
from .solution import parse_solution
from .utils import find_set, is_vrptw, parse_instance_name
from .vrptw import VRPTW, parse_vrptw


def read(instance_path: str, solution_path: Optional[str] = None):
    """
    Load the instance (and optionally the solution) from the
    provided path.
    """
    with open(instance_path, "r") as fi:
        lines = [l for l in (line.strip() for line in fi) if l]

    instance_name = parse_instance_name(lines)
    set_name = find_set(instance_name)

    instance: Union[VRPTW, Instance]

    if is_vrptw(set_name):
        instance = parse_vrptw(lines)
    else:
        instance = parse_cvrp(lines)

    if solution_path is not None:
        with open(solution_path, "r") as fi:
            lines = list(fi.read().splitlines())
            solution = parse_solution(lines)

        return instance, solution

    return instance
