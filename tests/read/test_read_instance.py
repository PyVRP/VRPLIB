import numpy as np
from numpy.testing import assert_equal, assert_raises
from pytest import mark

from vrplib.read import read_instance


@mark.parametrize("instance_format", ["CVRPLIB", "LKH", "VRP"])
def test_raise_unknown_instance_format(tmp_path, instance_format):
    """
    Tests if a ValueError is raised when an unknown instance format is passed.
    """
    path = tmp_path / "tmp.txt"
    path.write_text("test")

    with assert_raises(ValueError):
        read_instance(path, instance_format)


def test_read_vrplib_instance(tmp_path):
    """
    Tests if a VRPLIB instance is correctly read and parsed.
    """
    name = "test.sol"

    with open(tmp_path / name, "w") as fi:
        instance = "\n".join(
            [
                "NAME: VRPLIB",
                "EDGE_WEIGHT_TYPE: EXPLICIT",
                "EDGE_WEIGHT_FORMAT: FULL_MATRIX",
                "EDGE_WEIGHT_SECTION",
                "0  1",
                "1  0",
                "SERVICE_TIME_SECTION",
                "1  1",
                "TIME_WINDOW_SECTION",
                "1  1   2",
                "EOF",
            ]
        )
        fi.write(instance)

    desired = {
        "name": "VRPLIB",
        "edge_weight_type": "EXPLICIT",
        "edge_weight_format": "FULL_MATRIX",
        "edge_weight": np.array([[0, 1], [1, 0]]),
        "service_time": np.array([1]),
        "time_window": np.array([[1, 2]]),
    }

    assert_equal(read_instance(tmp_path / name), desired)


_SOLOMON_INSTANCE = [
    "C101",
    "VEHICLE",
    "NUMBER     CAPACITY",
    "25         200",
    "CUSTOMER",
    "CUST NO.  XCOORD.   YCOORD.  DEMAND   READY TIME  DUE DATE  SERVICE TIME",
    "0      40         50          0          0       1236          0",
    "1      45         68         10        912        967         90",
]


def test_read_solomon_instance(tmp_path):
    """
    Tests if a Solomon instance is correctly read and parsed.
    """
    name = "test.sol"

    with open(tmp_path / name, "w") as fi:
        instance = "\n".join(_SOLOMON_INSTANCE)
        fi.write(instance)

    dist = ((40 - 45) ** 2 + (50 - 68) ** 2) ** 0.5  # from 0 to 1
    desired = {
        "name": "C101",
        "vehicles": 25,
        "capacity": 200,
        "node_coord": np.array([[40, 50], [45, 68]]),
        "demand": np.array([0, 10]),
        "time_window": np.array([[0, 1236], [912, 967]]),
        "service_time": np.array([0, 90]),
        "edge_weight": np.array([[0, dist], [dist, 0]]),
    }

    actual = read_instance(tmp_path / name, instance_format="solomon")
    assert_equal(actual, desired)
