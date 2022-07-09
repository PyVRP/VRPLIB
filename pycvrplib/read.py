from typing import Optional

from .parse_instance import parse_instance
from .parse_solution import parse_solution
from .utils import strip_lines


def read(instance_path: str, solution_path: Optional[str] = None):
    """
    Read the instance (and optionally the solution) from the provided paths.
    """
    with open(instance_path, "r") as fi:
        instance = parse_instance(strip_lines(fi))

    if solution_path is None:
        return instance

    else:
        with open(solution_path, "r") as fi:
            solution = parse_solution(strip_lines(fi))

        return instance, solution
