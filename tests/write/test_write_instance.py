import numpy as np
from numpy.testing import assert_equal
from pytest import mark

from vrplib import write_instance


@mark.parametrize(
    "key, value, desired",
    (
        ["name", "Instance", "name: Instance"],  # string
        ["DIMENSION", 100, "DIMENSION: 100"],  # int
        ["VEHICLES", -10, "VEHICLES: -10"],  # negative
        ["CAPACITY", 10.5, "CAPACITY: 10.5"],  # float
        ["EMPTY", "", "EMPTY: "],  # empty
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
        # 1-dimensional list
        ["X_SECTION", [0, 10], "\n".join(["X_SECTION", "1\t0", "2\t10"])],
        # 1-dimensional list with mixed int and float values
        ["X_SECTION", [0, 10.5], "\n".join(["X_SECTION", "1\t0", "2\t10.5"])],
        # 1-dimensional list empty
        ["X_SECTION", [], "\n".join(["X_SECTION"])],
        # 2-dimensional numpy array
        [
            "Y_SECTION",
            np.array([[0, 0], [1, 1]]),
            "\n".join(["Y_SECTION", "1\t0\t0", "2\t1\t1"]),
        ],
        # 2-dimensional list empty
        ["Y_SECTION", [[]], "\n".join(["Y_SECTION", "1\t"])],
        # 2-dimensional array with different row lengths
        # NOTE: This is currently an invalid VRPLIB format, see
        # https://github.com/leonlan/VRPLIB/issues/108.
        [
            "DATA_SECTION",
            [[1], [3, 4]],
            "\n".join(["DATA_SECTION", "1\t1", "2\t3\t4"]),
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


def test_no_indices_depot_and_edge_weight_section(tmp_path):
    """
    Tests that indices are not included when formatting depot and edge weight
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
            [1, 1, 2],
            [1, 0, 3],
            [1, 3, 0],
        ]
    }
    write_instance(tmp_path / name, instance)

    desired = "\n".join(
        [
            "EDGE_WEIGHT_SECTION",
            "1\t1\t2",
            "1\t0\t3",
            "1\t3\t0",
            "EOF",
            "",
        ]
    )
    with open(tmp_path / name, "r") as fh:
        assert_equal(fh.read(), desired)


def test_small_instance_example(tmp_path):
    """
    Tests if writing a small instance yields the correct result.
    """
    name = "C101"
    instance = {
        "NAME": name,
        "TYPE": "VRPTW",
        "DIMENSION": 4,
        "CAPACITY": 200,
        "NODE_COORD_SECTION": [
            [40, 50],
            [45, 68],
            [45, 70],
            [42, 66],
        ],
        "DEMAND_SECTION": [0, 10, 30, 10],
        "DEPOT_SECTION": [1],
    }

    write_instance(tmp_path / name, instance)

    desired = "\n".join(
        [
            "NAME: C101",
            "TYPE: VRPTW",
            "DIMENSION: 4",
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
            "DEPOT_SECTION",
            "1",
            "EOF",
            "",
        ]
    )

    with open(tmp_path / name, "r") as fh:
        assert_equal(fh.read(), desired)
