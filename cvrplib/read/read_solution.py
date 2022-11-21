from .parse_solution import parse_solution
from .utils import strip_lines


def read_solution(path: str):
    """
    Read the solution from the passed-in path.
    """
    with open(path, "r") as fi:
        solution = parse_solution(strip_lines(fi))

    return solution
