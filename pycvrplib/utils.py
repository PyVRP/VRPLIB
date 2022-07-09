import inspect
import re
from itertools import combinations
from math import sqrt
from typing import Dict, List

from .constants import CVRP_SETS, DIMACS_names, XXL_names


def find_set(instance_name: str) -> str:
    """
    Find the set name of the instance.

    Notes
    -----
    - VRPTW instances start with "C, R, RC" directly followed by 1 or 2.
        HG instances have underscores ("_") in the name, whereas Solomon instances do not.
    - CVRP instance names and their corresponding set names share the same first letter.
        the exceptions are XXL and DIMACS instances, which have unique instance names
    """
    if re.match("(R|C|RC)[12]", instance_name):
        if "_" in instance_name:
            return "HG"
        else:
            return "Solomon"

    if any([instance_name.startswith(xxl) for xxl in XXL_names]):
        return "XXL"

    if any([instance_name.startswith(dimacs) for dimacs in DIMACS_names]):
        return "D"

    for set_name in CVRP_SETS:
        if instance_name.startswith(set_name):
            return set_name

    raise ValueError(f"Set name not known for instance: {instance_name}.")


def is_vrptw(name: str) -> bool:
    """
    Checks if the passed-in name is a VRPTW instance or not. Otherwise the instance
    is a CVRP instance.
    """
    return find_set(name) in ["HG", "Solomon"]


def from_dict_to_dataclass(cls, data: Dict):
    """
    Creates a class using the passed-in data dictionary.
    """
    return cls(
        **{
            key: (data[key] if val.default == val.empty else data.get(key, val.default))
            for key, val in inspect.signature(cls).parameters.items()
        }
    )


def euclidean(coords: List[List[int]], round_func=round) -> List[List[int]]:
    """
    Compute the pairwise Euclidean distances using the passed-in coordinates.
    `round_func` can be used to specify the rouding function. Default is to
    round to the nearest integer.
    """

    def dist(p, q):
        """
        Return the Euclidean distance between two coordinates.
        """
        return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))

    n = len(coords)
    distances = [[0 for _ in range(n)] for _ in range(n)]

    for (i, coord_i), (j, coord_j) in combinations(enumerate(coords), r=2):
        d_ij = round_func(dist(coord_i, coord_j))
        distances[i][j] = d_ij
        distances[j][i] = d_ij

    return distances


def strip_lines(lines):
    """
    Strip all lines and return the non-empty ones.
    """
    return [l for l in (line.strip() for line in lines) if l]
