import numpy as np
from numpy.testing import assert_equal

from vrplib.parse.parse_solomon import parse_solomon

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
