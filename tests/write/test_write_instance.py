import pytest
from numpy.testing import assert_equal

from cvrplib import read_instance, write_instance

from .._utils import selected_cases


def test_dummy_instance(tmp_path):
    """
    Tests if writing a small dummy instance yields the correct result.
    """
    name = "C101"
    instance = dict(
        name=name,
        type="VRPTW",
        dimension=101,
        capacity=200,
        node_coord=[[40, 50], [45, 68], [45, 70], [42, 66]],
        demand=[0, 10, 30, 10],
    )

    write_instance(tmp_path / name, instance)

    target = "\n".join(
        [
            "NAME : C101",
            "TYPE : VRPTW",
            "DIMENSION : 101",
            "CAPACITY : 200",
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

    with open(tmp_path / name, "r") as fi:
        assert_equal(fi.read(), target)


@pytest.mark.parametrize("case", selected_cases())
def test_write_read_vrplib_instance(tmp_path, case):
    """
    Tests if writing a VRPLIB instance and reading it yields the same result.
    """
    desired = read_instance(case.instance_path)

    write_instance(tmp_path / case.instance_name, desired)
    actual = read_instance(tmp_path / case.instance_name)

    assert_equal(actual, desired)


# TODO Test LKH-3 instances
