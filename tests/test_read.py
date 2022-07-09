import pytest

from cvrplib import read

from ._utils import compute_distance, selected_cases


@pytest.mark.parametrize("case", selected_cases())
def test_read(case):
    """
    Read the case and verify a subest its attributes.
    """
    instance, solution = read(case.instance_path, case.solution_path)

    assert instance.name == case.instance_name
    assert instance.dimension == case.dimension
    assert instance.capacity == case.capacity
    assert solution.cost == case.cost


@pytest.mark.parametrize("case", selected_cases())
def test_solution_cost(case):
    """
    Test if the proviced cost of the solution is the same as the cost
    calculated directly from the instance distances.

    We only test instances where the convention is to use integral distances.
    """
    instance, solution = read(case.instance_path, case.solution_path)

    if solution.cost % 1 == 0:
        assert pytest.approx(solution.cost) == compute_distance(
            instance, solution.routes
        )
