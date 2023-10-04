import numpy as np
from numpy.testing import assert_equal
from pytest import mark

from vrplib import write_instance


@mark.parametrize(
    "key, value, desired",
    (
        ["NAME", "Instance", "NAME: Instance"],
        ["type", "VRPTW", "type: VRPTW"],
        ["DIMENSION", 100, "DIMENSION: 100"],
        ["CAPACITY", -10.1, "CAPACITY: -10.1"],
        ["EMPTY", "", "EMPTY: "],
    ),
)
def test_specifications(tmp_path, key, value, desired):
    """
    Tests that key-value pairs where values are floats or strings are
    formatted as specifications.
    """
    name = "specifications"
    instance = {key: value}
    write_instance(tmp_path / name, instance)

    desired = "\n".join([desired, "EOF", ""])
    with open(tmp_path / name, "r") as fh:
        assert_equal(fh.read(), desired)


@mark.parametrize(
    "key, value, desired",
    (
        # list
        [
            "DEMAND_SECTION",
            [0, 10],
            "\n".join(["DEMAND_SECTION", "1\t0", "2\t10"]),
        ],
        # list of lists
        [
            "NODE_COORD_SECTION",
            [[0, 0], [1, 1]],
            "\n".join(["NODE_COORD_SECTION", "1\t0\t0", "2\t1\t1"]),
        ],
    ),
)
def test_sections(tmp_path, key, value, desired):
    """
    Tests that key-value pairs where values are lists are formatted as
    sections.
    """
    name = "sections"
    instance = {key: value}
    write_instance(tmp_path / name, instance)

    with open(tmp_path / name, "r") as fh:
        assert_equal(fh.read(), "\n".join([desired, "EOF", ""]))

    # Should also work if the values are numpy arrays.
    instance = {key: np.array(value)}
    write_instance(tmp_path / name, instance)

    with open(tmp_path / name, "r") as fh:
        assert_equal(fh.read(), "\n".join([desired, "EOF", ""]))


def test_no_indices_depot_and_edge_weight_section(tmp_path):
    """
    Tests that no indices are added when writing the depot and edge weight
    section.
    """
    # Let's first test the depot section.
    name = "depot"
    instance = {"DEPOT_SECTION": [1, 2]}
    write_instance(tmp_path / name, instance)

    desired = "\n".join(["DEPOT_SECTION", "1", "2", "EOF", ""])
    with open(tmp_path / name, "r") as fh:
        assert_equal(fh.read(), desired)

    # Now let's test the edge weight section.
    name = "edge_weight"
    instance = {
        "EDGE_WEIGHT_SECTION": [
            [0, 1, 2],
            [1, 0, 3],
            [2, 3, 0],
        ]
    }
    write_instance(tmp_path / name, instance)

    desired = "\n".join(
        [
            "EDGE_WEIGHT_SECTION",
            "0\t1\t2",
            "1\t0\t3",
            "2\t3\t0",
            "EOF",
            "",
        ]
    )
    with open(tmp_path / name, "r") as fh:
        assert_equal(fh.read(), desired)


def test_small_full_example(tmp_path):
    """
    Tests if writing a small instance yields the correct result.
    """
    name = "C101"
    instance = {
        "NAME": name,
        "TYPE": "VRPTW",
        "DIMENSION": 101,
        "CAPACITY": 200,
        "NODE_COORD_SECTION": [
            [40, 50],
            [45, 68],
            [45, 70],
            [42, 66],
        ],
        "DEMAND_SECTION": [0, 10, 30, 10],
    }

    write_instance(tmp_path / name, instance)

    desired = "\n".join(
        [
            "NAME: C101",
            "TYPE: VRPTW",
            "DIMENSION: 101",
            "CAPACITY: 200",
            "NODE_COORD_SECTION",
            "1\t40\t50",
            "2\t45\t68",
            "3\t45\t70",
            "4\t42\t66",
            "DEMAND_SECTION",
            "1\t0",
            "2\t10",
            "3\t30",
            "4\t10",
            "EOF",
            "",
        ]
    )

    with open(tmp_path / name, "r") as fh:
        assert_equal(fh.read(), desired)
