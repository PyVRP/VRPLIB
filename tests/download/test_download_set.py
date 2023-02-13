from numpy.testing import assert_equal, assert_raises

from vrplib.download import download_set

from ..utils import CVRPLIB_DATA_DIR


def test_raise_invalid_set_name():
    """
    Test if an error is raised when the passed-in set name is invalid.
    """
    with assert_raises(ValueError):
        download_set("invalid_name", "tmp")


def test_download_X_set(tmp_path):
    """
    Tests if the complete Solomon set is downloaded succesfully from CVRPLIB.
    """
    download_set("X", tmp_path)

    # Check that all Solomon instances and solutions are included
    for path in (CVRPLIB_DATA_DIR / "Vrp-Set-X").glob("*"):
        with open(tmp_path / path.name, "r") as fi:
            actual = fi.read()

        with open(path, "r") as fi:
            desired = fi.read()

        assert_equal(actual, desired)


def test_download_solomon_set(tmp_path):
    """
    Tests if the complete Solomon set is downloaded succesfully from CVRPLIB.
    """
    download_set("Solomon", tmp_path)

    # Check that all Solomon instances and solutions are included
    for path in (CVRPLIB_DATA_DIR / "Vrp-Set-Solomon").glob("*"):
        with open(tmp_path / path.name, "r") as fi:
            actual = fi.read()

        with open(path, "r") as fi:
            desired = fi.read()

        assert_equal(actual, desired)
