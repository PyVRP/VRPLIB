from typing import Any, Dict, List

import numpy as np

from .parse_distances import euclidean
from .parse_utils import text2lines


def parse_solomon(text: str, distance_rounding=None):
    """
    Parse the text of a Solomon VRPTW instance.

    text
        The instance text.
    distance_rounding
        A custom distance rounding function. The default is to follow the
        VRPLIB convention, see ... # TODO
    """
    lines = text2lines(text)

    data: Dict[str, Any] = {"name": lines[0]}
    data.update(parse_vehicles(lines))
    data.update(parse_customers(lines, distance_rounding))

    return data


def parse_vehicles(lines: List[str]) -> Dict:
    data = {}
    data["n_vehicles"], data["capacity"] = [
        int(num) for num in lines[3].split()
    ]
    return data


def parse_customers(lines: List[str], distance_rounding=None) -> Dict:
    data = {}

    A = np.genfromtxt(lines[6:], dtype=int)
    n_customers = A.shape[0] - 1

    data["node_coord"] = A[:, 1:3]
    data["dimension"] = n_customers + 1
    data["demands"] = A[:, 3]
    data["n_customers"] = n_customers
    data["customers"] = list(range(1, n_customers + 1))
    data["earliest"] = A[:, 4]
    data["latest"] = A[:, 5]
    data["service_times"] = A[:, 6]

    round_func = (
        distance_rounding if callable(distance_rounding) else lambda x: x
    )
    data["distances"] = euclidean(data["node_coord"], round_func)

    return data
