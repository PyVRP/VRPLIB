import pytest
from numpy.testing import assert_equal

from cvrplib import read_instance, write_instance

from .._utils import selected_cases


def test_write_dummy_instance(tmp_path):
    """
    Tests if writing a small dummy instance is done correctly.

    TODO Can we take an instance for write_instance?
    Is there a distinction between specs and sections?
    """
    name = "C101"

    specs = dict(name=name, type="VRPTW", dimension=101, capacity=200)
    sections = dict(
        node_coord=[[40, 50], [45, 68], [45, 70], [42, 66]],
        demand=[0, 10, 30, 10],
    )
    write_instance(tmp_path / name, specs, sections)

    with open(tmp_path / name, "r") as fi:
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

        assert_equal(fi.read(), target)


@pytest.mark.parametrize("case", selected_cases())
def test_write_real_instance(tmp_path, case):
    """
    Test an original VRPLIB instance.
    """
    original = read_instance(case.instance_path)
    print(original.keys())

    specs = [
        "name",
        "capacity",
        "dimension",
        "type",
        "comment",
        "edge_weight_type",
        "edge_weight_format",
        "node_coord_type",
        "service_time",
        "display_data_type",
        "distance",
    ]
    write_instance(
        tmp_path / case.instance_name,
        {k: v for k, v in original.items() if k in specs},
        {k: v for k, v in original.items() if k not in specs},
    )
    new = read_instance(tmp_path / case.instance_name)

    assert_equal(original, new)
