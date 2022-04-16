import pytest
import glob

from ..Parser import parse_instance, Instance


def instance_paths(set_names: list[str]):
    return [
        path
        for set_name in set_names
        for path in glob.iglob(f"./data/**/{set_name}/**/*.vrp", recursive=True)
    ]


@pytest.mark.parametrize("path", instance_paths(["A", "B", "D", "M"]))
def test_instance(path):
    """
    Test parsering CVRPLIB instances.
    """
    instance = parse_instance(path)
    assert instance
    assert isinstance(instance, Instance)
