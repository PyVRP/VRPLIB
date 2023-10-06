from numpy.testing import assert_equal, assert_raises
from pytest import mark

from vrplib import write_solution


@mark.parametrize(
    "routes, desired",
    [
        ([[1, 2]], "Route #1: 1 2"),
        ([[1, 2], [42, 9]], "Route #1: 1 2\nRoute #2: 42 9"),
    ],
)
def test_write_routes(tmp_path, routes, desired):
    """
    Tests the writing of a solution with routes.
    """
    name = "test.sol"
    write_solution(tmp_path / name, routes)

    with open(tmp_path / name, "r") as fh:
        assert_equal(fh.read(), desired + "\n")


def test_raise_empty_routes(tmp_path):
    """
    Tests that an error is raised if a route is empty.
    """
    name = "test.sol"

    with assert_raises(ValueError):
        write_solution(tmp_path / name, [[]])

    with assert_raises(ValueError):
        write_solution(tmp_path / name, [[1], []])


@mark.parametrize(
    "data, desired",
    [
        ({"Cost": 100}, "Cost: 100"),  # int
        ({"Time": 123.45}, "Time: 123.45"),  # float
        ({"Distance": -1}, "Distance: -1"),  # negative int
        ({"name": "test.sol"}, "name: test.sol"),  # string
        ({"Vehicle types": [1, 2, 3]}, "Vehicle types: [1, 2, 3]"),  # list
        ({"Vehicle types": (1, 3)}, "Vehicle types: (1, 3)"),  # tuple
    ],
)
def test_format_other_data(tmp_path, data, desired):
    name = "test.sol"
    routes = [[1]]
    write_solution(tmp_path / name, routes, data)

    with open(tmp_path / name, "r") as fh:
        text = "Route #1: 1" + "\n" + desired + "\n"
        assert_equal(fh.read(), text)


def test_small_example(tmp_path):
    """
    Tests the writing of a small example.
    """
    name = "test.sol"
    routes = [[1, 2], [3, 4], [5]]
    data = {"Cost": 100, "Time": 123.45, "name": name}

    write_solution(tmp_path / name, routes, data)

    desired = "\n".join(
        [
            "Route #1: 1 2",
            "Route #2: 3 4",
            "Route #3: 5",
            "Cost: 100",
            "Time: 123.45",
            "name: test.sol",
            "",
        ]
    )

    with open(tmp_path / name, "r") as fh:
        assert_equal(fh.read(), desired)
