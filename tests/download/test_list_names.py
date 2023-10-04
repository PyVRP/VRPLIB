import pytest
from numpy.testing import assert_

from vrplib import list_names

from ..utils import selected_cases


def test_deprecationg_warning():
    """
    Check if the deprecation warning is raised.
    """
    with pytest.warns(DeprecationWarning):
        list_names(1, 2, "cvrp")


@pytest.mark.filterwarnings("ignore:The function")
@pytest.mark.parametrize("case", selected_cases())
def test_list_names(case):
    assert_(case.instance_name in list_names())


@pytest.mark.filterwarnings("ignore:The function")
@pytest.mark.parametrize(
    "low, high, vrp_type",
    [
        (1, 2, "vrp"),  # vrp not in [None, 'cvrp', 'vrptw']
    ],
)
def test_list_names_raise(low, high, vrp_type):
    """
    Raise for invalid input paramaters.
    """
    with pytest.raises(ValueError):
        list_names(low, high, vrp_type)


@pytest.mark.filterwarnings("ignore:The function")
@pytest.mark.parametrize(
    "name, low, high, vrp_type",
    [
        ("A-n32-k5", 31, 31, "cvrp"),
        ("ORTEC-n242-k12", 0, 241, "cvrp"),
        ("Flanders2", 30000, None, "cvrp"),
        ("X-n101-k25", 0, 100, None),
        ("RC208", 0, 100, "vrptw"),
        ("RC2_10_10", 1000, 1000, None),
    ],
)
def test_list_names_n(name, low, high, vrp_type):
    """
    Check if the passed-in name is in the list of names.
    """
    assert_(name in list_names(low, high, vrp_type))
