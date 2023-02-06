import pytest
from numpy.testing import assert_equal

from vrplib import download_instance


def test_raise_invalid_name():
    """
    Raise an error if the passed-in name is invalid.
    """
    with pytest.raises(ValueError):
        download_instance("invalid_name", "tmp")


def test_download_vrplib_instance(tmp_path):
    """
    Tests if a VRPLIB instance is correctly downloaded from CVRPLIB.
    """
    name = "X-n101-k25"
    ext = ".vrp"
    loc = tmp_path / (name + ext)

    download_instance(name, loc)

    with open(loc, "r") as fi:
        actual = fi.read()

    with open(f"data/cvrplib/{name + ext}", "r") as fi:
        desired = fi.read()

    assert_equal(actual, desired)


def test_download_solomon_instance(tmp_path):
    """
    Tests if a Solomon instance is correctly downloaded from CVRPLIB.
    """
    name = "C101"
    ext = ".txt"
    loc = tmp_path / (name + ext)

    download_instance(name, loc)

    with open(loc, "r") as fi:
        actual = fi.read()

    with open(f"data/cvrplib/{name + ext}", "r") as fi:
        desired = fi.read()

    assert_equal(actual, desired)
