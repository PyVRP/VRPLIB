import os

from numpy.testing import assert_, assert_equal, assert_raises

from vrplib import download_solution


def test_raise_invalid_name():
    """
    Raise an error if the passed-in name is invalid.
    """
    with assert_raises(ValueError):
        download_solution("invalid_name", "tmp")


def test_download_vrplib_solution_file_name_path(tmp_path):
    """
    Tests if a VRPLIB solution is correctly downloaded from CVRPLIB.
    """
    name = "X-n101-k25"
    fname = "random_file_name.txt"

    download_solution(name, tmp_path / fname)

    expected_path = tmp_path / fname
    assert_(os.path.exists(expected_path))

    with open(expected_path, "r") as fi:
        actual = fi.read()

    # The best known solution is known to be optimal, so the the solution
    # file in the repository will not be outdated.
    with open(f"tests/data/cvrplib/{name}.sol", "r") as fi:
        desired = fi.read()

    assert_equal(actual, desired)


def test_download_vrplib_solution_dir_path(tmp_path):
    """
    Tests if a VRPLIB solution is correctly downloaded from CVRPLIB.
    """
    name = "X-n101-k25"

    download_solution(name, tmp_path)

    expected_path = tmp_path / (name + ".sol")
    assert_(os.path.exists(expected_path))

    with open(expected_path, "r") as fi:
        actual = fi.read()

    # The best known solution is known to be optimal, so the the solution
    # file in the repository will not be outdated.
    with open(f"tests/data/cvrplib/{name}.sol", "r") as fi:
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

    # The best known solution is known to be optimal, so the the solution
    # file in the repository will not be outdated.
    with open(f"tests/data/cvrplib/{name + ext}", "r") as fi:
        desired = fi.read()

    assert_equal(actual, desired)
