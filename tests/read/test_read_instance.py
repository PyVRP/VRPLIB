import numpy as np
from numpy.testing import assert_, assert_equal, assert_raises
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


_VRPLIB_INSTANCE = [
    "NAME: VRPLIB",
    "EDGE_WEIGHT_TYPE: EUC_2D",
    "NODE_COORD_SECTION",
    "1  0  0",
    "2  0  1",
    "SERVICE_TIME_SECTION",
    "1  1",
    "TIME_WINDOW_SECTION",
    "1  1   2",
    "EOF",
]


def test_read_vrplib_instance(tmp_path):
    """
    Tests if a VRPLIB instance is correctly read and parsed.
    """
    name = "vrplib.txt"

    with open(tmp_path / name, "w") as fi:
        instance = "\n".join(_VRPLIB_INSTANCE)
        fi.write(instance)

    desired = {
        "name": "VRPLIB",
        "edge_weight_type": "EUC_2D",
        "node_coord": np.array([[0, 0], [0, 1]]),
        "service_time": np.array([1]),
        "time_window": np.array([[1, 2]]),
        "edge_weight": np.array([[0, 1], [1, 0]]),
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
    name = "solomon.txt"

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


def test_do_not_compute_edge_weights(tmp_path):
    """
    Tests if the edge weights are not computed when the corresponding argument
    is set to False.
    """
    # Test for VRPLIB instance
    name = "vrplib.txt"

    with open(tmp_path / name, "w") as fi:
        instance = "\n".join(_VRPLIB_INSTANCE)
        fi.write(instance)

    instance = read_instance(tmp_path / name, compute_edge_weights=False)
    assert_("edge_weight" not in instance)

    # Test for Solomon instance
    name = "solomon.txt"

    with open(tmp_path / name, "w") as fi:
        instance = "\n".join(_SOLOMON_INSTANCE)
        fi.write(instance)

    instance = read_instance(
        tmp_path / name, instance_format="solomon", compute_edge_weights=False
    )
    assert_("edge_weight" not in instance)
