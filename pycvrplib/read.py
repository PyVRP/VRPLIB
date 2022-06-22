from typing import Optional

from ._parse_utils import parse_instance
from .solution import parse_solution


def read(instance_path: str, solution_path: Optional[str] = None):
    """
    Load the instance (and optionally the solution) from the
    provided path.
    """
    with open(instance_path, "r") as fi:
        lines = list(fi.read().splitlines())

    instance = parse_instance(lines)

    if solution_path is not None:
        with open(solution_path, "r") as fi:
            lines = list(fi.read().splitlines())
            solution = parse_solution(lines)

        return instance, solution

    return instance
