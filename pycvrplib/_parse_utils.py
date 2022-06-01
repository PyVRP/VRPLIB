from __future__ import annotations

import math
import inspect
import re
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from typing import Any, Dict, List, Optional, Union

from .constants import DEPOT, SHIFT

"""
Instance utilities
"""


def parse_instance(lines: List[str]) -> Instance:
    """
    Parse the lines of an instance, consisting of:
    - metadata [dimension, edge_weight_type, etc.]
    - sections [coords, demands, etc.]

    Moreover, additional data is created, e.g., distances data.
    """
    data = {}
    data.update(parse_metadata(lines))
    data.update(parse_sections(lines))
    data.update(parse_distances(data))

    return from_dict_to_dataclass(Instance, data)


def parse_metadata(lines: List[str]) -> Dict[str, Any]:
    """
    Parse the metadata at the beginning of the instance file.
    This data is formatted as KEY : VALUE lines.
    """
    data = {}
    for line in lines:
        if ": " in line:
            k, v = [x.strip() for x in re.split("\\s*: ", line, maxsplit=1)]
            data[k.lower()] = int(v) if v.isnumeric() else v
    return data


def parse_sections(lines: List[str]) -> Dict[str, Any]:
    """
    Parse the sections data of the instance file. Sections start with a row
    containing NAME_SECTION followed by a number of lines with data.
    """
    name = None  # Used as key to store data
    sections = defaultdict(list)

    for line in lines:
        if "_SECTION" in line:
            name = line.split("_SECTION")[0].strip()

        elif "EOF" in line:
            continue

        elif name:
            row = [float(num) for num in line.strip().split()]
            sections[name].append(row)

    data: Dict[str, Any] = {}

    for name, section in sections.items():
        if name == "DEMAND":
            data["demands"] = [int(row[1]) for row in section]

        elif name == "DEPOT":
            data["depot"] = int(section[0][0]) + SHIFT

        elif name == "NODE_COORD":
            data["coordinates"] = [[int(row[1]), int(row[2])] for row in section]

        elif name == "EDGE_WEIGHT":
            data["edge_weight"] = [[int(num) for num in row] for row in section]

    return data


def parse_distances(data: Dict[str, Any]) -> Dict[str, List[List[int]]]:  # type: ignore[return]
    """
    Create distances data.

    Using the metadata "edge_weight_type" we can infer how to construct the
    distances: 1) either by computing the pairwise Euclidan distances
    using the provided coordinates or by 2) using the triangular matrix.
    """

    if "distances" not in data:
        if data["edge_weight_type"] == "EUC_2D":
            return {"distances": euclidean(data["coordinates"])}

        elif data["edge_weight_type"] == "EXPLICIT":
            if data["edge_weight_format"] == "LOWER_ROW":
                lr_repr = get_representation(data["edge_weight"], n=data["dimension"])

                if lr_repr == "flattened":
                    return {
                        "distances": from_flattened(
                            data["edge_weight"], n=data["dimension"]
                        )
                    }

                elif lr_repr == "triangular":
                    return {"distances": from_triangular(data["edge_weight"])}


def get_representation(edge_weights: List[List[int]], n: int) -> str:
    """
    Returns the representation type in which the lower row data is given.

    Some instances have a flattened representation, e.g., E-n13-k4,
    whereas others have a triangular repr, e.g., ORTEC-n242-k12.

    """
    if len(edge_weights) == n - 1:
        return "triangular"
    else:
        return "flattened"


def euclidean(coords: List[List[int]]) -> List[List[int]]:
    """
    Compute the pairwise Euclidean distances using the passed-in coordinates.
    """

    def dist(p, q):
        """
        Return the Euclidean distance between to coordinates.
        """
        return math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))

    n = len(coords)
    distances = [[0 for _ in range(n)] for _ in range(n)]

    for (i, coord_i), (j, coord_j) in combinations(enumerate(coords), r=2):
        d_ij = round(dist(coord_i, coord_j))
        distances[i][j] = d_ij
        distances[j][i] = d_ij

    return distances


def from_triangular(triangular: List[List[int]]) -> List[List[int]]:
    """
    Compute a full distances matrix from a triangular matrix.
    """
    n = len(triangular) + 1
    distances = [[0 for _ in range(n)] for _ in range(n)]

    for j, i in combinations(range(n), r=2):
        t_ij = triangular[i - 1][j]
        distances[i][j] = t_ij
        distances[j][i] = t_ij

    return distances


def from_flattened(edge_weights: List[List[int]], n: int) -> List[List[int]]:
    """
    Compute a full distances matrix from a flattened lower row representation.

    The numbers in a flattened list correspond the matrix element indices
    (1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2), (4, 0), ...
    """
    distances = [[0 for _ in range(n)] for _ in range(n)]
    flattened = [distance for distances in edge_weights for distance in distances]
    indices = sorted([(i, j) for (j, i) in combinations(range(n), r=2)])

    for idx, (i, j) in enumerate(indices):
        d_ij = flattened[idx]
        distances[i][j] = d_ij
        distances[j][i] = d_ij

    return distances


def from_dict_to_dataclass(cls, data):
    return cls(
        **{
            key: (data[key] if val.default == val.empty else data.get(key, val.default))
            for key, val in inspect.signature(cls).parameters.items()
        }
    )


@dataclass
class Instance:
    name: str
    comment: str
    dimension: int
    capacity: int
    distances: List[List[float]]
    demands: List[int]
    depot: int
    coordinates: Optional[List[List[float]]] = None


"""
Solution utilities
"""


def parse_solution(lines: List[str]) -> Solution:
    """
    Extract the solution. Solutions contain routes, which are indexed
    from 1 to n.
    """

    def parse_routes(lines: List[str]) -> List[List[int]]:
        """
        Parse the lines to obtain the routes.
        """
        routes = []

        for line in lines:
            line = line.strip().lower()

            if "route" in line:
                # TODO Split is not necessary; can match directly
                route = re.split(r"route #\d+: ", line)[1]
                route = [int(cust) + (1 + SHIFT) for cust in route.split(" ") if cust]
                routes.append(route)

        return routes

    def parse_cost(lines: List[str]) -> float:
        for line in lines:
            line = line.strip().lower()

            if "cost" in line:
                cost = line.lstrip("cost ")
                break

        return int(cost) if cost.isdigit() else float(cost)

    data: Dict[str, Any] = {}
    data["routes"] = parse_routes(lines)
    data["cost"] = parse_cost(lines)

    return from_dict_to_dataclass(Solution, data)


@dataclass
class Solution:
    routes: List[int]
    cost: float
