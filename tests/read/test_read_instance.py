import numpy as np
import pytest
from numpy.testing import assert_equal, assert_raises

from vrplib.read import read_instance


@pytest.mark.parametrize("instance_format", ["CVRPLIB", "LKH", "VRP"])
def test_raise_unknown_instance_format(tmp_path, instance_format):
    """
    Tests if a ValueError is raised when an unknown instance format is passed.
    """
    path = tmp_path / "tmp.txt"
    path.write_text("test")

    with assert_raises(ValueError):
        read_instance(path, instance_format)


def test_read_vrplib_instance(tmp_path):
    """
    Tests if a VRPLIB instance is correctly read and parsed.
    """
    name = "test.sol"

    with open(tmp_path / name, "w") as fi:
        instance = "\n".join(
            [
                "NAME: VRPLIB",
                "EDGE_WEIGHT_TYPE: EXPLICIT",
                "EDGE_WEIGHT_FORMAT: FULL_MATRIX",
                "EDGE_WEIGHT_SECTION",
                "0  1",
                "1  0",
                "SERVICE_TIME_SECTION",
                "1  1",
                "TIME_WINDOW_SECTION",
                "1  1   2",
                "EOF",
            ]
        )
        fi.write(instance)

    target = dict(
        name="VRPLIB",
        edge_weight_type="EXPLICIT",
        edge_weight_format="FULL_MATRIX",
        edge_weight=np.array([[0, 1], [1, 0]]),
        service_time=np.array([1]),
        time_window=np.array([[1, 2]]),
    )

    assert_equal(read_instance(tmp_path / name), target)


def test_read_solomon_instance(tmp_path):
    """
    Tests if a Solomon instance is correctly read and parsed.
    """
    name = "test.sol"

    with open(tmp_path / name, "w") as fi:
        instance = "\n".join(
            [
                "NAME: VRPLIB",
                "EDGE_WEIGHT_TYPE: EXPLICIT",
                "EDGE_WEIGHT_FORMAT: FULL_MATRIX",
                "EDGE_WEIGHT_SECTION",
                "0  1",
                "1  0",
                "SERVICE_TIME_SECTION",
                "1  1",
                "TIME_WINDOW_SECTION",
                "1  1   2",
                "EOF",
            ]
        )
        fi.write(instance)

    target = dict(
        name="VRPLIB",
        edge_weight_type="EXPLICIT",
        edge_weight_format="FULL_MATRIX",
        edge_weight=np.array([[0, 1], [1, 0]]),
        service_time=np.array([1]),
        time_window=np.array([[1, 2]]),
    )

    assert_equal(read_instance(tmp_path / name), target)
