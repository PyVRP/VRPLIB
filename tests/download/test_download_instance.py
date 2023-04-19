import os

import pytest
from numpy.testing import assert_, assert_equal

from vrplib import download_instance


def test_raise_invalid_name():
    """
    Raise an error if the passed-in name is invalid.
    """
    with pytest.raises(ValueError):
        download_instance("invalid_name", "tmp")


def test_download_vrplib_instance_file_name(tmp_path):
    """
    Tests if a VRPLIB instance is correctly downloaded from CVRPLIB
    and saved to the passed-in file path.
    """
    name = "X-n101-k25"
    fname = "random_file_name.txt"

    download_instance(name, tmp_path / fname)

    expected_path = tmp_path / fname
    assert_(os.path.exists(expected_path))

    with open(expected_path, "r") as fi:
        actual = fi.read()

    with open(f"tests/data/cvrplib/{name}.vrp", "r") as fi:
        desired = fi.read()

    assert_equal(actual, desired)


def test_download_vrplib_instance_dir_path(tmp_path):
    """
    Tests if a VRPLIB instance is correctly downloaded from CVRPLIB
    and saved to the passed-in directory.
    """
    name = "X-n101-k25"

    download_instance(name, tmp_path)

    expected_path = tmp_path / (name + ".vrp")
    assert_(os.path.exists(expected_path))

    with open(expected_path, "r") as fi:
        actual = fi.read()

    with open(f"tests/data/cvrplib/{name}.vrp", "r") as fi:
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

    with open(f"tests/data/cvrplib/{name + ext}", "r") as fi:
        desired = fi.read()

    assert_equal(actual, desired)
