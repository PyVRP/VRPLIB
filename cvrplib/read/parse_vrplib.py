from __future__ import annotations

import math
import re
from collections import defaultdict
from itertools import combinations
from typing import Any, Dict, List

import numpy as np

from .utils import euclidean


def parse_vrplib(lines: List[str]):
    """
    Parse the lines of an instance, consisting of:
    - specifications [dimension, edge_weight_type, etc.]
    - data sections [coords, demands, etc.]
    - distances
    """
    data = parse_specifications(lines)
    data.update(parse_sections(lines))

    distances = parse_distances(data)
    data.update(distances if distances else {})

    return data


def parse_specifications(lines: List[str]) -> Dict[str, Any]:
    """
    Parse the problem specifications. These are lines that are formatted as
    KEY : VALUE.
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
            break

        elif name is not None:
            row = [_int_or_float(num) for num in line.split()]

            # Most sections start with an index that we do not want to keep
            if name not in ["EDGE_WEIGHT", "DEPOT"]:
                row = row[1:]

            sections[name].append(row)

    data: Dict[str, Any] = {}

    for section_name, section_data in sections.items():
        section_name = section_name.lower()

        if section_name == "depot":
            depot_data = np.array(section_data)
            depot_data[:-1] -= 1  # normalize to zero-based indices
            data[section_name] = depot_data
        elif section_name == "edge_weight":
            data[section_name] = section_data
        else:
            array = np.array(section_data)
            array = array.reshape(-1) if array.shape[1] == 1 else array

            data[section_name] = array

    return data


def parse_distances(data: Dict[str, Any]) -> Dict[str, List[List[int]]]:  # type: ignore[return] # noqa: E501
    """
    Create distances data.

    Using the specification "edge_weight_type" we can infer how to construct
    the distances: 1) either by computing the pairwise Euclidan distances
    using the provided coordinates or by 2) using the triangular matrix.
    """

    if "distances" not in data:
        if data["edge_weight_type"] in ["EUC_2D"]:
            return {"distances": euclidean(data["node_coord"])}

        elif data["edge_weight_type"] in ["FLOOR_2D"]:
            return {"distances": euclidean(data["node_coord"], math.floor)}

        elif data["edge_weight_type"] in ["EXACT_2D"]:
            return {"distances": euclidean(data["node_coord"], lambda n: n)}

        elif data["edge_weight_type"] == "EXPLICIT":
            if data["edge_weight_format"] == "LOWER_ROW":
                lr_repr = get_representation(
                    data["edge_weight"], n=data["dimension"]
                )

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
    flattened = [
        distance for distances in edge_weights for distance in distances
    ]
    indices = sorted([(i, j) for (j, i) in combinations(range(n), r=2)])

    for idx, (i, j) in enumerate(indices):
        d_ij = flattened[idx]
        distances[i][j] = d_ij
        distances[j][i] = d_ij

    return distances


def _int_or_float(num: str):
    """Return an integer if num is an integer string and float otherwise."""
    return int(num) if num.isnumeric() else float(num)
