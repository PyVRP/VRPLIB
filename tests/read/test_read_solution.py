from pathlib import Path

import pytest

from cvrplib import read_solution

from .._utils import LKH_3_DATA_DIR, selected_cases


@pytest.mark.parametrize("case", selected_cases())
def test_read_solution(case):
    """
    Read the case solution and verify its cost.
    """
    solution = read_solution(case.solution_path)
    assert solution["cost"] == pytest.approx(case.cost, 2)


@pytest.mark.parametrize(
    "path", Path(LKH_3_DATA_DIR).glob("*/SOLUTIONS/*.sol")
)
def test_lkh_3_vrplib(path):
    """
    TODO Maybe add more solutions
    TODO Test for solution values
    """
    read_solution(path)
