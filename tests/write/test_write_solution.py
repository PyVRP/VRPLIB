from pathlib import Path

import pytest
from numpy.testing import assert_equal

from cvrplib import read_solution, write_solution

from .._utils import LKH_3_DATA_DIR, selected_cases


def test_dummy(tmp_path):
    """
    Tests if writing a dummy solution yields the correct result.
    """
    name = "test.sol"
    data = dict(
        routes=[[1, 2], [3, 4], [5]],
        cost=100,
        time=123.45,
        name=name,
    )

    write_solution(tmp_path / name, **data)

    target = "\n".join(
        [
            "Route #1: 1 2",
            "Route #2: 3 4",
            "Route #3: 5",
            "cost: 100",
            "time: 123.45",
            "name: test.sol",
            "",
        ]
    )

    with open(tmp_path / name, "r") as fi:
        assert_equal(fi.read(), target)


@pytest.mark.parametrize("case", selected_cases()[:2])
def test_cvrplib(tmp_path, case):
    """
    Tests if writing a CVRPLIB instance and reading it yields the same result.
    """
    desired = read_solution(case.solution_path)

    write_solution(tmp_path / "test.sol", **desired)
    actual = read_solution(tmp_path / "test.sol")

    assert_equal(actual, desired)


@pytest.mark.parametrize(
    "solution_path", Path(LKH_3_DATA_DIR).glob("*/SOLUTIONS/*.sol")
)
def test_lkh_3(tmp_path, solution_path):
    """
    Tests if writing a LKH-3 instance and reading it yields the same result.
    """
    desired = read_solution(solution_path)

    write_solution(tmp_path / "test.sol", **desired)
    actual = read_solution(tmp_path / "test.sol")

    assert_equal(actual, desired)
