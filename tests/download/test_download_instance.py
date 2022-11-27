import pytest

from cvrplib import download_instance

from .._utils import selected_cases


# Only test the first two CVRP and VRPTW instances because it takes time
@pytest.mark.parametrize(
    "case", [selected_cases()[num] for num in [0, 1, -2, -1]]
)
def test_download_instance(case):
    """
    Download the case instance.
    """
    instance = download_instance(case.instance_name)
    assert instance["name"] == case.instance_name
    assert instance["dimension"] == case.dimension
    assert instance["capacity"] == case.capacity


def test_raise_invalid_name():
    """
    Raise an error if the passed-in name is invalid.
    """
    with pytest.raises(ValueError):
        download_instance("invalid_name")
