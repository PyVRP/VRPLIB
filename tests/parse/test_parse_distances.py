import numpy as np
import pytest
from numpy.testing import assert_almost_equal, assert_equal, assert_raises

from vrplib.parse.parse_distances import parse_distances


@pytest.mark.parametrize(
    "edge_weight_type, edge_weight_format",
    [
        ("2D", ""),  # unknown 2D type
        ("EXPLICIT", ""),  # explicit without format
        ("IMPLICIT", "LOWER_ROW"),  # unknown type
        ("TEST", "ABCD"),  # unknown type and format
    ],
)
def test_unknown_edge_weight_type_and_format(
    edge_weight_type, edge_weight_format
):
    """
    Tests if an error is raised when an unknown edge weight type and edge
    weight format are specified.
    """
    instance = {
        "edge_weight_type": edge_weight_type,
        "edge_weight_format": edge_weight_format,
    }
    with pytest.raises(ValueError):
        parse_distances([], **instance)


@pytest.mark.parametrize(
    "edge_weight_type", ["EUC_2D", "FLOOR_2D", "CEIL_2D", "EXACT_2D"]
)
def test_raise_no_coordinates_euclidean_distances(edge_weight_type):
    """
    Tests if a ValueError is raised when no node coordinates are given when
    an Euclidean edge weight type is specified.
    """
    with assert_raises(ValueError):
        parse_distances([], edge_weight_type)


@pytest.mark.parametrize(
    "edge_weight_type, desired",
    [
        ("EUC_2D", [[0, np.sqrt(2)], [np.sqrt(2), 0]]),
        ("FLOOR_2D", [[0, 1], [1, 0]]),
        ("CEIL_2D", [[0, 2], [2, 0]]),
        ("EXACT_2D", [[0, 1414], [1414, 0]]),
    ],
)
def test_parse_euclidean_distances(edge_weight_type, desired):
    """
    Tests that an array of node coordinates is correctly transformed into
    a Euclidean distance matrix according to the weight type specification.
    """
    actual = parse_distances(
        [], edge_weight_type, node_coord=np.array([[0, 0], [1, 1]])
    )

    assert_almost_equal(actual, desired)


@pytest.mark.parametrize(
    "data",
    [
        [[1, 2, 3, 4, 5, 6]],  # single line
        [[1, 2, 3, 4], [5, 6]],  # ragged lines
        [[1], [2, 3], [4, 5, 6]],  # proper triangular rows
    ],
)
def test_parse_lower_row(data):
    """
    Tests that LOWER_ROW instances are parsed correctly regardless of how
    the values are wrapped across lines. See #134.
    """
    data = np.array(data, dtype=object)
    actual = parse_distances(
        data,
        edge_weight_type="EXPLICIT",
        edge_weight_format="LOWER_ROW",
    )
    desired = np.array(
        [
            [0, 1, 2, 4],
            [1, 0, 3, 5],
            [2, 3, 0, 6],
            [4, 5, 6, 0],
        ]
    )

    assert_equal(actual, desired)
