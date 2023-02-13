import numpy as np
import pytest
from numpy.testing import assert_almost_equal, assert_equal, assert_raises

from vrplib.parse.parse_distances import (
    from_eilon,
    from_lower_row,
    is_triangular_number,
    parse_distances,
)


@pytest.mark.parametrize("edge_weight_type", ["EUC_4D", "MANHATTAN", "Lnorm"])
def test_unknown_edge_weight_type(edge_weight_type):
    instance = {"edge_weight_type": edge_weight_type}
    with pytest.raises(ValueError):
        parse_distances([], **instance)


@pytest.mark.parametrize("edge_weight_format", ["", "empty", "HALF_MATRIX"])
def test_unknown_explicit_edge_weight_format(edge_weight_format):
    """
    Tests if an error is raised when an unknown edge weight format is specified
    together with an ``EXPLICIT`` edge weight type.
    """
    instance = {
        "edge_weight_type": "EXPLICIT",
        "edge_weight_format": edge_weight_format,
    }
    with pytest.raises(ValueError):
        parse_distances([], **instance)


@pytest.mark.parametrize(
    "edge_weight_type, edge_weight_format",
    [("", ""), ("IMPLICIT", "LOWER_ROW"), ("TEST", "ABCD")],
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
    "edge_weight_type", ["EUC_2D", "FLOOR_2D", "EXACT_2D"]
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


@pytest.mark.parametrize("comment", ["Eilon", "", "None"])
def test_parse_lower_row(comment):
    """
    Tests if a ``LOWER ROW`` instance is parsed as Eilon instance or regular
    instance. Eilon instances do not contain a proper lower row matrix, but
    a lower column matrix instead. The current way of detecting an Eilon
    instance is by means of the ``COMMENT`` field, which is checked for
    including "Eilon".
    """
    instance = {
        "data": np.array([[1], [2, 3], [4, 5, 6]], dtype=object),
        "edge_weight_type": "EXPLICIT",
        "edge_weight_format": "LOWER_ROW",
        "comment": comment,
    }

    if "Eilon" in comment:
        desired = np.array(
            [
                [0, 1, 2, 3],
                [1, 0, 4, 5],
                [2, 4, 0, 6],
                [3, 5, 6, 0],
            ]
        )
    else:
        desired = np.array(
            [
                [0, 1, 2, 4],
                [1, 0, 3, 5],
                [2, 3, 0, 6],
                [4, 5, 6, 0],
            ]
        )

    assert_equal(parse_distances(**instance), desired)


def test_from_lower_row():
    """
    Tests that a lower row triangular matrix is correctly transformed into a
    full matrix.
    """
    triangular_matrix = np.array([[1], [2, 3], [4, 5, 6]], dtype=object)
    actual = from_lower_row(triangular_matrix)
    desired = np.array(
        [
            [0, 1, 2, 4],
            [1, 0, 3, 5],
            [2, 3, 0, 6],
            [4, 5, 6, 0],
        ]
    )

    assert_equal(actual, desired)


def test_from_eilon():
    """
    Tests that the distance matrix of Eilon instances is correctly transformed.
    These distance matrices have entries corresponding to the lower column
    triangular matrices. But the distance matrix is not a triangular matrix,
    so they are flattened first.
    """
    eilon = np.array([[1, 2, 3, 4], [5, 6]], dtype=object)
    actual = from_eilon(eilon)
    desired = np.array(
        [
            [0, 1, 2, 3],
            [1, 0, 4, 5],
            [2, 4, 0, 6],
            [3, 5, 6, 0],
        ]
    )

    assert_equal(actual, desired)


@pytest.mark.parametrize(
    "n, res", [(1, True), (3, True), (4, False), (630, True), (1000, False)]
)
def test_is_triangular_number(n, res):
    assert_equal(is_triangular_number(n), res)
