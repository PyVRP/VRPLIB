"""
Shared utility functions.
"""
import inspect
from itertools import combinations
from math import sqrt
from typing import List


def from_dict_to_dataclass(cls, data):
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
        Return the Euclidean distance between to coordinates.
        """
        return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))

    n = len(coords)
    distances = [[0 for _ in range(n)] for _ in range(n)]

    for (i, coord_i), (j, coord_j) in combinations(enumerate(coords), r=2):
        d_ij = round_func(dist(coord_i, coord_j))
        distances[i][j] = d_ij
        distances[j][i] = d_ij

    return distances
