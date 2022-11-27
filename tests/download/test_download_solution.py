import pytest

from cvrplib import download_solution

from .._utils import selected_cases


# Only test the first two CVRP and VRPTW instances because it takes time
@pytest.mark.parametrize(
    "case", [selected_cases()[num] for num in [0, 1, -2, -1]]
)
def test_download_solution(case):
    """
    Download the case solution.
    """
    solution = download_solution(case.instance_name)
    assert solution["cost"] == pytest.approx(case.cost, 2)


def test_raise_invalid_name():
    """
    Raise an error if the passed-in name is invalid.
    """
    with pytest.raises(ValueError):
        download_solution("invalid_name")
