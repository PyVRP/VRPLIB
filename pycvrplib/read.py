from typing import Optional

from .parse_instance import parse_instance
from .parse_solution import parse_solution


def read(instance_path: str, solution_path: Optional[str] = None):
    """
    Load the instance (and optionally the solution) from the
    provided paths.
    """
    with open(instance_path, "r") as fi:
        instance = parse_instance(_read_nonempty_lines(fi))

    if solution_path is None:
        return instance

    else:
        with open(solution_path, "r") as fi:
            solution = parse_solution(_read_nonempty_lines(fi))

        return instance, solution


def _read_nonempty_lines(fi):
    return [l for l in (line.strip() for line in fi) if l]
