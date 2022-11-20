from numpy.testing import assert_array_equal
from numpy.testing._private.utils import assert_almost_equal

from cvrplib import read

from .._utils import CVRPLIB_DATA_DIR, LKH_3_DATA_DIR


# TODO Make these tests better formatted
def test_CVRPLIB_X_n101_k25():
    instance = read(CVRPLIB_DATA_DIR / "X-n101-k25.vrp")

    assert instance["name"] == "X-n101-k25"
    assert instance["dimension"] == 101
    assert instance["capacity"] == 206
    assert instance["demands"][100] == 35
    assert_almost_equal(instance["node_coord"][100], [615, 750])


def test_CVRPLIB_CMT6():
    """
    CMT6 instance contains the fields ``distance_limit`` and ``service_time``.
    """
    instance = read(CVRPLIB_DATA_DIR / "CMT6.vrp")
    N = 50

    assert instance["name"] == "CMT6"
    assert instance["dimension"] == N + 1
    assert instance["capacity"] == 160
    assert instance["demands"][N] == 10
    assert_almost_equal(instance["node_coord"][N], [56, 37])


def test_LKH_3_X_n101_k25():
    instance = read(LKH_3_DATA_DIR / "CVRP/INSTANCES/Uchoa/X-n101-k25.vrp")

    assert instance["name"] == "X-n101-k25"
    assert instance["dimension"] == 101
    assert instance["capacity"] == 206
    assert instance["demands"][100] == 35
    assert_almost_equal(instance["node_coord"][100], [615, 750])


def test_LKH_3_CMT6():
    instance = read(LKH_3_DATA_DIR / "CVRP/INSTANCES/CMT/CMT6.vrp")
    N = 50

    depot = instance["depot"]
    assert instance["name"] == "CMT6"
    assert instance["dimension"] == N + 1
    assert instance["capacity"] == 160
    assert instance["distance"] == 200
    assert instance["demands"][depot] == 0
    assert_array_equal(instance["node_coord"][depot], [30.0, 40.0])
