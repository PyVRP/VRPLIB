from typing import Callable, Dict, Optional, Union, no_type_check

import numpy as np

from .parse_distances import euclidean
from .parse_utils import text2lines

Instance = Dict[str, Union[str, int, float, np.ndarray]]


@no_type_check  # typing bug in mypy, see below
def parse_solomon(
    text: str, distance_rounding: Optional[Callable] = None
) -> Instance:
    """
    Parses the text of a Solomon VRPTW instance.

    Parameters
    ----------
    text
        The instance text.
    distance_rounding
        A custom distance rounding function. The default is to follow the
        VRPLIB convention, see ... # TODO
    """
    lines = text2lines(text)

    instance: Instance = {"name": lines[0]}
    instance["n_vehicles"], instance["capacity"] = [
        int(num) for num in lines[3].split()
    ]

    data = np.genfromtxt(lines[6:], dtype=int)

    instance["node_coord"] = data[:, 1:3]
    instance["demands"] = data[:, 3]
    instance["earliest"] = data[:, 4]
    instance["latest"] = data[:, 5]
    instance["service_times"] = data[:, 6]

    # Bug in mypy: https://github.com/python/mypy/issues/4134
    instance["distances"] = euclidean(
        instance["node_coord"],
        distance_rounding if distance_rounding is not None else _identity,
    )

    return instance


def _identity(x):
    return x
