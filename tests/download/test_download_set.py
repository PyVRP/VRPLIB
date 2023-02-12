from numpy.testing import assert_equal, assert_raises
from vrplib.download import download_set


def test_raise_invalid_set_name():
    """
    Test if an error is raised when the passed-in set name is invalid.
    """
    with assert_raises(ValueError):
        download_set("invalid_name", "tmp")


def test_download_solomon_set(tmp_path):
    """
    Tests if the coplete Solomon set is downloaded succesfully from CVRPLIB.
    """
    download_set("Solomon", tmp_path)

    # Check that all Solomon instances and solutions are included
