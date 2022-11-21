import pytest

from cvrplib import read_solution

from .._utils import selected_cases


@pytest.mark.parametrize("case", selected_cases())
def test_read_solution(case):
    """
    Read the case solution and verify its cost.
    """
    solution = read_solution(case.solution_path)
    assert solution["cost"] == pytest.approx(case.cost, 2)
