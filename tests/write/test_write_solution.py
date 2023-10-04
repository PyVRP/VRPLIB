from numpy.testing import assert_equal

from vrplib import write_solution


def test_write_solution(tmp_path):
    """
    Tests the write_solution function.
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
