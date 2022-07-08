from functools import lru_cache
from typing import Optional

from .utils import find_set, is_vrptw


def list_names(
    low: int = 0,
    high: Optional[int] = None,
    vrp_type: Optional[str] = None,
):
    """
    Return the names of instances.
    with n_customers between [low, high].

    Params
    ------
    - low
        The minimum number of customers
    - high
        The maximum number of customers
    - vrp_type
        The vrp_type, one of ['cvrp', 'vrptw']. If unspecified, then
        both cvrp and vrptw instances are returned.
    """
    instances = _parse_instance_names()

    instances = [inst for inst in instances if inst["n_customers"] >= low]

    if high is not None:
        instances = [inst for inst in instances if inst["n_customers"] <= high]

    if vrp_type is not None:
        if vrp_type not in ["cvrp", "vrptw"]:
            raise ValueError("vrp_type must be one of ['cvrp', 'vrptw']")
        elif vrp_type == "cvrp":
            instances = [inst for inst in instances if not is_vrptw(inst["name"])]
        else:
            instances = [inst for inst in instances if is_vrptw(find_set(inst["name"]))]

    return [inst["name"] for inst in instances]


@lru_cache()
def _parse_instance_names():
    with open("pycvrplib/instance_names.csv", "r") as fi:
        instances = [line.strip().split(",") for line in fi.readlines()]

    return [{"name": inst[0], "n_customers": int(inst[1])} for inst in instances]
