from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Instance:
    name: str
    dimension: int
    n_customers: int
    depot: int
    customers: List[int]
    capacity: int
    distances: List[List[float]]
    demands: List[int]
    service_times: List[float]
    coordinates: Optional[List[List[float]]]


@dataclass
class CVRP(Instance):
    distance_limit: float


@dataclass
class VRPTW(Instance):
    n_vehicles: int
    earliest: List[int]
    latest: List[int]
