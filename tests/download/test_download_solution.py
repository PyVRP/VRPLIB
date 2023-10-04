import os

import pytest
from numpy.testing import assert_, assert_equal, assert_raises

from vrplib import download_solution


def test_deprecation_warning():
    """
    Checks if a deprecation warning is raised when the function is called.
    """
    with pytest.warns(DeprecationWarning):
        download_solution("X-n101-k25", "tmp")


@pytest.mark.filterwarnings("ignore:The function")
def test_raise_invalid_name():
    """
    Raise an error if the passed-in name is invalid.
    """
    with assert_raises(ValueError):
        download_solution("invalid_name", "tmp")


@pytest.mark.filterwarnings("ignore:The function")
def test_download_vrplib_solution_file_name_path(tmp_path):
    """
    Tests if a VRPLIB solution is correctly downloaded from CVRPLIB
    and saved to the passed-in file path.
    """
    name = "X-n101-k25"
    fname = "random_file_name.txt"
    file_path = tmp_path / fname

    download_solution(name, file_path)
    assert_(os.path.exists(file_path))

    with open(file_path, "r") as fi:
        actual = fi.read()

    # The best known solution is known to be optimal, so the solution
    # file in the repository will not be outdated.
    with open(f"tests/data/cvrplib/{name}.sol", "r") as fi:
        desired = fi.read()

    assert_equal(actual, desired)


@pytest.mark.filterwarnings("ignore:The function")
def test_download_vrplib_solution_dir_path(tmp_path):
    """
    Tests if a VRPLIB solution is correctly downloaded from CVRPLIB
    and saved to the passed-in directory.
    """
    name = "X-n101-k25"
    dir_path = tmp_path
    file_path = dir_path / (name + ".sol")

    download_solution(name, dir_path)
    assert_(os.path.exists(file_path))

    with open(file_path, "r") as fi:
        actual = fi.read()

    # The best known solution is known to be optimal, so the solution
    # file in the repository will not be outdated.
    with open(f"tests/data/cvrplib/{name}.sol", "r") as fi:
        desired = fi.read()

    assert_equal(actual, desired)


@pytest.mark.filterwarnings("ignore:The function")
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

    # The best known solution is known to be optimal, so the solution
    # file in the repository will not be outdated.
    with open(f"tests/data/cvrplib/{name + ext}", "r") as fi:
        desired = fi.read()

    assert_equal(actual, desired)
