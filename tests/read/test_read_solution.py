from numpy.testing import assert_equal

from cvrplib import read_solution


def test_read_dummy_solution(tmp_path):
    """
    Tests if a dummy solution is correctly read and parsed.
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
