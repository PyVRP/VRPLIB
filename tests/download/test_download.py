import pytest

from cvrplib import download

from .._utils import selected_cases


# Only test the first two CVRP and VRPTW instances because it takes time
@pytest.mark.filterwarnings("ignore:cvrplib.download")
@pytest.mark.parametrize(
    "case", [selected_cases()[num] for num in [0, 1, -2, -1]]
)
def test_download(case):
    """
    Download the case instance and solution.
    """
    instance, solution = download(case.instance_name, solution=True)
    assert instance["name"] == case.instance_name
    assert instance["dimension"] == case.dimension
    assert instance["capacity"] == case.capacity
    assert solution["cost"] == pytest.approx(case.cost, 2)


@pytest.mark.filterwarnings("ignore:cvrplib.download")
def test_raise_invalid_name():
    """
    Raise an error if the passed-in name is invalid.
    """
    with pytest.raises(ValueError):
        download("invalid_name", solution=True)


@pytest.mark.parametrize("case", selected_cases())
def test_download_deprecated(case):
    download.cache_clear()

    with pytest.deprecated_call():
        download(case.instance_name, solution=True)
