from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

import numpy as np

from .constants import DEPOT
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

    data["coordinates"] = A[:, 1:3]
    data["dimension"] = n_customers + 1
    data["demands"] = A[:, 3]
    data["n_customers"] = n_customers
    data["customers"] = np.arange(1, n_customers + 1)
    data["earliest_times"] = A[:, 4]
    data["latest_times"] = A[:, 5]
    data["service_times"] = A[:, 6]
    data["distances"] = euclidean(data["coordinates"].tolist(), lambda di: round(di, 1))

    return data


@dataclass
class VRPTW:
    name: str
    dimension: int
    n_customers: int
    depot: int
    customers: List[int]
    n_vehicles: int
    capacity: int
    distances: List[List[float]]
    coordinates: List[List[float]]
    demands: List[int]
    service_times: List[int]
    earliest_times: List[int]
    latest_times: List[int]
