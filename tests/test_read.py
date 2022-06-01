import pytest

from pycvrplib import read
from ._utils import compute_distance, selected_cases


@pytest.mark.parametrize("case", selected_cases())
def test_read(case):
    """
    Download the A_n32_k5 instance and solution.
    """
    instance, solution = read(case.instance_path, case.solution_path)

    assert instance.name == case.instance_name
    assert instance.dimension == case.dimension
    assert instance.capacity == case.capacity
    assert solution.cost == case.cost


@pytest.mark.parametrize("case", selected_cases())
def test_distances(case):
    """
    Test if the cost of the provided solution corresponds to the one
    computed using the read instance.

    We only test instances where the convention is to use integral distances.
    """
    instance, solution = read(case.instance_path, case.solution_path)

    if solution.cost % 1 == 0:
        assert pytest.approx(solution.cost) == compute_distance(
            instance, solution.routes
        )
