from itertools import combinations
from math import sqrt
from typing import List


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


def text2lines(text: str) -> List[str]:
    """
    Takes a text and returns a list of non-empty, stripped lines.
    """
    return [line.strip() for line in text.splitlines() if line.strip()]


def infer_type(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s