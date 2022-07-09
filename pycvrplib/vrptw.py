from __future__ import annotations

from typing import Any, Dict, List

import numpy as np

from .constants import DEPOT
from .Instance import VRPTW
from .utils import euclidean, from_dict_to_dataclass


def parse_vrptw(lines: List[str]) -> VRPTW:
    """
    Parse the lines of a VRPTW instance.
    """
    data: Dict[str, Any] = {}
    data["name"] = lines[0]
    data["depot"] = DEPOT

    data.update(parse_vehicles(lines))
    data.update(parse_customers(lines))

    return from_dict_to_dataclass(VRPTW, data)


def parse_vehicles(lines: List[str]) -> Dict:
    data = {}
    data["n_vehicles"], data["capacity"] = [int(num) for num in lines[3].split()]
    return data


def parse_customers(lines: List[str]) -> Dict:
    data = {}

    A = np.genfromtxt(lines[6:], dtype=int)
    n_customers = A.shape[0] - 1

    data["coordinates"] = A[:, 1:3].tolist()
    data["dimension"] = n_customers + 1
    data["demands"] = A[:, 3].tolist()
    data["n_customers"] = n_customers
    data["customers"] = list(range(1, n_customers + 1))
    data["earliest"] = A[:, 4].tolist()
    data["latest"] = A[:, 5].tolist()
    data["service_times"] = A[:, 6].tolist()
    data["distances"] = euclidean(data["coordinates"])

    return data
