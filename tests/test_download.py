import pytest

from pycvrplib import download

from ._utils import selected_cases


# Only test the first two because it takes time to download
@pytest.mark.parametrize("case", selected_cases()[:2])
def test_download(case):
    """
    Download the case instance and solution.
    """
    instance, solution = download(case.name, solution=True)
    assert instance.name == case.instance_name
    assert instance.dimension == case.dimension
    assert instance.capacity == case.capacity
    assert solution.cost == pytest.approx(case.cost, 2)


def test_raise_invalid_name():
    """
    Raise an error if the passed-in name is invalid.
    """
    with pytest.raises(ValueError):
        instance, solution = download("invalid_name", solution=True)
