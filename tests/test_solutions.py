import pytest
import glob

from ..Parser import parse_solution, Solution


def solution_paths(set_names: list[str]):
    return [
        path
        for set_name in set_names
        for path in glob.iglob(f"./data/**/{set_name}/**/*.sol", recursive=True)
    ]


@pytest.mark.parametrize("path", solution_paths(["A", "E", "D", "M", "XXL"]))
def test_solution(path):
    """
    Test loading all pglib_opf_*.m instances.
    Assumes that all the instances are in the pglib-opf directory.
    """
    solution = parse_solution(path)

    assert solution
    assert isinstance(solution, Solution)
