import numpy as np
import pytest
from numpy.testing import assert_array_equal, assert_equal

from cvrplib.read import read_instance

from .._utils import CVRPLIB_DATA_DIR

# TODO Rename "cvrp" to VRPLIB
# TODO Add more tests to this

instances = [
    (
        CVRPLIB_DATA_DIR / "X-n101-k25.vrp",
        {
            "name": "X-n101-k25",
            "type": "CVRP",
            "dimension": 101,
            "capacity": 206,
        },
        {
            "node_coord": [365, 689],
            "demand": 0,
            "depot": 0,
        },
    ),
    (
        CVRPLIB_DATA_DIR / "tai75a.vrp",
        {
            "name": "Tai75a",
            "type": "CVRP",
            "dimension": 76,
            "capacity": 1445,
            "edge_weight_type": "EUC_2D",
        },
        {
            "node_coord": [0, 0],
            "demand": 0,
            "depot": 0,
        },
    ),
]


@pytest.mark.parametrize("path, specifications, sections", instances)
def test_read_instance_vrplib(path, specifications, sections):
    instance = read_instance(path)

    for k, v in specifications.items():
        assert_equal(instance[k], v)

    for k, v in sections.items():
        if np.isscalar(instance[k]):
            assert_equal(instance[k], v)
        else:
            # Always test for first element in data arrays
            assert_array_equal(instance[k][0], v)


# def test_read_instance_solomon(path, specifications, sections):
#     # instance = read(path)
#     pass
