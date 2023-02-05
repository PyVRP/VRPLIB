import pytest
from numpy.testing import assert_equal

from vrplib.parse.parse_solution import parse_solution


@pytest.mark.parametrize(
    "text, data",
    [
        (
            "Route #1: 1 2 3\n Route #2: 5 6\n COST: 10",
            {"routes": [[1, 2, 3], [5, 6]], "cost": 10},
        ),
        (
            "Route #1: 1 \n Route #2: 6\n comment: VRPLIB",
            {"routes": [[1], [6]], "comment": "VRPLIB"},
        ),
        (
            "Route #1: 1 \n Route #2: 6\n time 180.23",
            {"routes": [[1], [6]], "time": 180.23},
        ),
    ],
)
def test_parse_solution(text, data):
    """
    Tests if a solution is correctly parsed.
    """
    assert_equal(parse_solution(text), data)
