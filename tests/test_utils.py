import pytest
from ._utils import selected_cases
from pycvrplib.utils import find_set


@pytest.mark.parametrize("case", selected_cases())
def test_find_dir(case):
    assert find_set(case.instance_name) == case.set_name


def test_raise_invalid_name():
    with pytest.raises(ValueError):
        assert find_set("test_name")
