from pathlib import Path

import numpy as np
from numpy.testing import assert_equal, assert_raises
from pytest import mark

from vrplib.parse.parse_solomon import parse_solomon

_DATA_DIR = Path("tests/data")
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


@mark.parametrize(
    "name",
    [
        "C101.sol",  # solution file
        "A-n32-k5.vrp",
        "B-n31-k5.vrp",
        "CMT6.vrp",
        "E-n13-k4.vrp",
        "F-n72-k4.vrp",
        "Golden_1.vrp",
        "Li_21.vrp",
        "ORTEC-n242-k12.vrp",
        "P-n16-k8.vrp",
        "X-n101-k25.vrp",
    ],
)
def test_raise_invalid_solomon_instance(name):
    with assert_raises(RuntimeError):
        with open(_DATA_DIR / name, "r") as fh:
            parse_solomon(fh.read())


@mark.parametrize("name", ["C101.txt", "C1_2_1.txt"])
def test_does_not_raise(name):
    with open(_DATA_DIR / name, "r") as fh:
        parse_solomon(fh.read())


def test_parse_vrplib():
    """
    Checks if the Solomon instance lines are correctly parsed.
    """
    text = "\n".join(_SOLOMON_INSTANCE)

    actual = parse_solomon(text)

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

    assert_equal(actual, desired)
