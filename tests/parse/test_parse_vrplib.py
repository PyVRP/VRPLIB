from pathlib import Path

import numpy as np
from numpy.testing import assert_equal, assert_raises
from pytest import mark

from vrplib.parse.parse_vrplib import (
    group_specifications_and_sections,
    parse_section,
    parse_specification,
    parse_vrplib,
)

_DATA_DIR = Path("tests/data/")


@mark.parametrize(
    "name",
    [
        "C101.txt",  # solomon
        "C1_2_1.txt",  # solomon
        "C101.sol",  # solution
        "NoColonSpecification.txt",
    ],
)
def test_raise_invalid_vrplib_format(name):
    """
    Tests if a RuntimeError is raised when the text is not in VRPLIB format.
    """
    with open(_DATA_DIR / name, "r") as fh:
        with assert_raises(RuntimeError):
            parse_vrplib(fh.read())


@mark.parametrize(
    "name",
    [
        "A-n32-k5.vrp",
        "B-n31-k5.vrp",
        "CMT6.vrp",
        "E-n13-k4.vrp",
        "F-n72-k4.vrp",
        "Golden_1.vrp",
        "Li_21.vrp",
        "ORTEC-n242-k12.vrp",
        "P-n16-k8.vrp",
        "X-n101-k25.vrp",
    ],
)
def test_no_raise_valid_vrplib_format(name):
    with open(_DATA_DIR / name, "r") as fh:
        parse_vrplib(fh.read())


def test_group_specifications_and_sections():
    """
    Check if instance lines are correctly grouped into specifications
    and sections.
    """
    specs = [
        "NAME : ORTEC-VRPTW-ASYM-00c5356f-d1-n258-k12",
        "COMMENT : ORTEC",
    ]
    sections = [
        "EDGE_WEIGHT_SECTION",
        "0	1908",
        "1994	0",
        "TIME_WINDOW_SECTION",
        "1	0	41340",
        "2	15600	23100",
    ]

    lines = specs + sections + ["EOF"]
    actual_specs, actual_sections = group_specifications_and_sections(lines)

    assert_equal(actual_specs, specs)
    assert_equal(actual_sections, [sections[:3], sections[3:]])


@mark.parametrize(
    "line, key, value",
    [
        ("NAME : Antwerp 1", "name", "Antwerp 1"),  # Whitespace around :
        ("COMMENT:'test' ", "comment", "'test'"),  # No whitespace around :
        ("COMMENT: BKS:1", "comment", "BKS:1"),  # Split at first :
        ("CAPACITY: 30", "capacity", 30),  # int value
        ("CAPACITY: 30.5", "capacity", 30.5),  # float value
        ("name: Antwerp 1", "name", "Antwerp 1"),  # OK if key is not uppercase
    ],
)
def test_parse_specification(line, key, value):
    """
    Tests if a specification line is correctly parsed.
    """
    k, v = parse_specification(line)

    assert_equal(k, key)
    assert_equal(v, value)


@mark.parametrize(
    "lines, desired",
    [
        (
            ["SERVICE_TIME_SECTION", "1  2", "2  3", "3  100"],
            ["service_time", np.array([2, 3, 100])],
        ),
        (
            ["TIME_WINDOW_SECTION", "1  2  3", "2  1  2"],
            ["time_window", np.array([[2, 3], [1, 2]])],
        ),
        (
            ["DEMAND_SECTION", "1  1.1", "2  2.2", "3  3.3"],
            ["demand", np.array([1.1, 2.2, 3.3])],
        ),
        (
            ["DEPOT_SECTION", "1", "-1"],
            ["depot", np.array([0])],
        ),
        (
            ["UNKNOWN_SECTION", "1 1", "1 -1"],
            ["unknown", np.array([1, -1])],
        ),
    ],
)
def test_parse_section(lines, desired):
    """
    Tests if data sections (excluding edge weights) are parsed correctly.
    """
    actual = parse_section(lines, {})

    assert_equal(actual, desired)


@mark.parametrize(
    "lines",
    [
        ["DEPOT_SECTION"],
        ["DEPOT_SECTION", "1"],
        ["DEPOT_SECTION", "1", "-100"],
    ],
)
def test_depot_section_raise_runtime_error(lines):
    """
    Tests if a RuntimeError is raised when the depot section does not end
    with a -1.
    """
    with assert_raises(RuntimeError):
        parse_section(lines, {})


def test_parse_vrplib():
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
    actual = parse_vrplib(instance)

    desired = {
        "name": "VRPLIB",
        "edge_weight_type": "EXPLICIT",
        "edge_weight_format": "FULL_MATRIX",
        "edge_weight": np.array([[0, 1], [1, 0]]),
        "service_time": np.array([1]),
        "time_window": np.array([[1, 2]]),
    }

    assert_equal(actual, desired)


def test_parse_vrplib_no_explicit_edge_weights():
    """
    Tests if the edge weight section is calculated when the instance does not
    contain an explicit section.
    """
    instance = "\n".join(
        [
            "NAME: VRPLIB",
            "EDGE_WEIGHT_TYPE: FLOOR_2D",
            "NODE_COORD_SECTION",
            "1  0   1",
            "2  1   0",
            "SERVICE_TIME_SECTION",
            "1  1",
            "2  1",
            "TIME_WINDOW_SECTION",
            "1  1   2",
            "2  1   2",
            "EOF",
        ]
    )
    actual = parse_vrplib(instance)

    desired = {
        "name": "VRPLIB",
        "edge_weight_type": "FLOOR_2D",
        "edge_weight": np.array([[0, 1], [1, 0]]),
        "node_coord": np.array([[0, 1], [1, 0]]),
        "service_time": np.array([1, 1]),
        "time_window": np.array([[1, 2], [1, 2]]),
    }

    assert_equal(actual, desired)
