from typing import List, Optional, Union

from .cvrp import CVRP, parse_cvrp
from .parse_instance import parse_instance
from .parse_solution import parse_solution
from .vrptw import VRPTW, parse_vrptw


def read(instance_path: str, solution_path: Optional[str] = None):
    """
    Load the instance (and optionally the solution) from the
    provided paths.
    """
    with open(instance_path, "r") as fi:
        lines = [l for l in (line.strip() for line in fi) if l]

    instance = parse_instance(lines)

    if solution_path is not None:
        with open(solution_path, "r") as fi:
            lines = list(fi.read().splitlines())
            solution = parse_solution(lines)

        return instance, solution

    return instance
