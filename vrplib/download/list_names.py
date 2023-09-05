import importlib.resources as pkg_resource
from functools import lru_cache
from typing import Optional

from .download_utils import is_vrptw


def list_names(
    low: Optional[int] = None,
    high: Optional[int] = None,
    vrp_type: Optional[str] = None,
):
    """
    Returns the names of the instances that can be downloaded from CVRPLIB.

    Parameters
    ----------
    low
        The minimum number of customers of the listed instances.
    high
        The maximum number of customers of the listed instances.
    vrp_type
        The vrp_type, one of ['cvrp', 'vrptw']. If not set, then instances
        of both types are returned.
    """
    instances = _read_instance_data()

    if low is not None:
        instances = filter(lambda inst: inst["n_customers"] >= low, instances)

    if high is not None:
        instances = filter(lambda inst: inst["n_customers"] <= high, instances)

    if vrp_type not in [None, "cvrp", "vrptw"]:
        raise ValueError("vrp_type must be one of [None, 'cvrp', 'vrptw']")

    elif vrp_type == "cvrp":
        instances = filter(lambda inst: not is_vrptw(inst["name"]), instances)

    elif vrp_type == "vrptw":
        instances = filter(lambda inst: is_vrptw(inst["name"]), instances)

    return [inst["name"] for inst in instances]


@lru_cache()
def _read_instance_data():
    """
    Reads the instance data. All CVRPLIB instance names are stored in the
    `instance_data.csv` file.
    """
    fi = pkg_resource.read_text(__package__, "instance_data.csv")
    instances = [line.strip().split(",") for line in fi.split()]

    return [
        {"name": inst[0], "n_customers": int(inst[1])} for inst in instances
    ]
