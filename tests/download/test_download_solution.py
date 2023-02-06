import pytest
from numpy.testing import assert_equal

from vrplib import download_solution


def test_raise_invalid_name():
    """
    Raise an error if the passed-in name is invalid.
    """
    with pytest.raises(ValueError):
        download_solution("invalid_name", "tmp")


def test_download_vrplib_solution(tmp_path):
    """
    Tests if a VRPLIB solution is correctly downloaded from CVRPLIB.
    """
    name = "X-n101-k25"
    ext = ".sol"
    loc = tmp_path / (name + ext)

    download_solution(name, loc)

    with open(loc, "r") as fi:
        actual = fi.read()

    with open(f"data/cvrplib/{name + ext}", "r") as fi:
        desired = fi.read()

    assert_equal(actual, desired)


def test_download_solomon_solution(tmp_path):
    """
    Tests if a Solomon solution is correctly downloaded from CVRPLIB.
    """
    name = "C101"
    ext = ".sol"
    loc = tmp_path / (name + ext)

    download_solution(name, loc)

    with open(loc, "r") as fi:
        actual = fi.read()

    with open(f"data/cvrplib/{name + ext}", "r") as fi:
        desired = fi.read()

    assert_equal(actual, desired)
