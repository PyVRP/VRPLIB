import pytest

from pycvrplib import list_names

from ._utils import selected_cases


@pytest.mark.parametrize("case", selected_cases())
def test_list_names(case):
    names = list_names()
    assert case.instance_name in names


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
    Check if the passed-in name is in the list of names when low and high are passed.
    """
    assert name in list_names(low, high, vrp_type)
