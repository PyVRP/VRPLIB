import pytest
from numpy.testing import assert_almost_equal

from cvrplib.read import read_instance, read_solution

from .._utils import selected_cases


@pytest.mark.parametrize("case", selected_cases())
def test_solution_cost(case):
    """
    Tests if the proviced cost of the solution is the same as the cost
    calculated directly from the instance distances.
    """
    instance = read_instance(case.instance_path)
    solution = read_solution(case.solution_path)

    # Manually compute the distance from the instance and solution
    dist = instance["edge_weight"]
    cost = 0

    for route in solution["routes"]:
        visits = [0] + route + [0]
        for idx in range(len(route) + 1):
            cost += dist[visits[idx]][visits[idx + 1]]

    assert_almost_equal(cost, solution["cost"], decimal=2)


# TODO Add more tests!
