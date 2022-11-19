import pytest

from cvrplib.utils import find_set

from ._utils import selected_cases


@pytest.mark.parametrize("case", selected_cases())
def test_find_dir(case):
    assert find_set(case.instance_name) == case.set_name


def test_raise_invalid_name():
    with pytest.raises(ValueError):
        assert find_set("test_name")
