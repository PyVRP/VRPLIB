from pathlib import Path

import pytest
from numpy.testing import assert_equal

from cvrplib import read_solution

from .._utils import LKH_3_DATA_DIR, selected_cases


def test_dummy(tmp_path):
    """
    Tests if writing a dummy solution yields the correct result.
    """
    name = "test.sol"

    with open(tmp_path / name, "w") as fi:
        solution = "\n".join(
            [
                "Route 1 : 1 2",
                "Route 2 : 3 4",
                "Route 3 : 5",
                "Cost : 100",
                "Time : 123.45",
                "Name : test.sol",
                "Comment : Test.",
            ]
        )
        fi.write(solution)

    target = dict(
        routes=[[1, 2], [3, 4], [5]],
        cost=100,
        time=123.45,
        name=name,
        comment="Test.",
    )

    assert_equal(read_solution(tmp_path / name), target)


@pytest.mark.parametrize("case", selected_cases())
def test_read_solution(case):
    """
    Read the case solution and verify its cost.
    """
    solution = read_solution(case.solution_path)
    assert_equal(solution["cost"], case.cost)


@pytest.mark.parametrize(
    "path", Path(LKH_3_DATA_DIR).glob("*/SOLUTIONS/*.sol")
)
def test_lkh_3_vrplib(path):
    """
    TODO Maybe add more solutions
    TODO Test for solution values
    """
    read_solution(path)
