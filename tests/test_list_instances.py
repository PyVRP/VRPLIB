import pytest

from ._utils import compute_distance, selected_cases
from pycvrplib import list_instances


@pytest.mark.parametrize("case", selected_cases())
def test_list_instances(case):
    """
    Test if certain instances are shown in the value returned by the
    list_instances function.
    """
    names = list_instances()

    assert case.name in names
