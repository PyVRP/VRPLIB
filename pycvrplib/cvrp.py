from __future__ import annotations

import re
from collections import defaultdict
from itertools import combinations
from typing import Any, Dict, List

from .constants import DEPOT
from .Instance import CVRP
from .utils import euclidean, from_dict_to_dataclass


def parse_cvrp(lines: List[str]) -> CVRP:
    """
    Parse the lines of an instance, consisting of:
    - metadata [dimension, edge_weight_type, etc.]
    - sections [coords, demands, etc.]
    - distances
    """
    data = {}
    data.update(parse_metadata(lines))
    data.update(parse_sections(lines))
    data.update(parse_distances(data))

    return from_dict_to_dataclass(CVRP, data)


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

    data["depot"] = DEPOT
    data["n_customers"] = data["dimension"] - 1  # type: ignore
    data["customers"] = list(range(1, data["n_customers"] + 1))  # type: ignore
    data["distance_limit"] = float(data.get("distance", float("inf")))  # type: ignore
    data["service_times"] = [0.0] + [float(data.get("service_time", 0.0)) for _ in range(data["n_customers"])]  # type: ignore
    data["coordinates"] = None  # type: ignore

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

    Notes
    -----
    - Some instances have a flattened representation, e.g., E-n13-k4,
      whereas others have a triangular repr, e.g., ORTEC-n242-k12.
    """
    if len(edge_weights) == n - 1:
        return "triangular"
    else:
        return "flattened"


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
