from __future__ import annotations

import math
import re
from collections import defaultdict
from itertools import combinations
from typing import Any, Dict, List

import numpy as np

from .utils import euclidean, infer_type

Instance = Dict[str, Any]
Lines = List[str]


def parse_vrplib(lines: Lines, distance_rounding=None):
    """
    Parse the lines of an instance, consisting of:
    - specifications [dimension, edge_weight_type, etc.]
    - data sections [coords, demands, etc.]
    - distances
    """
    instance = parse_specifications(lines)
    instance.update(parse_sections(lines))

    distances = parse_distances(instance, distance_rounding)
    instance.update(distances if distances else {})

    return instance


def parse_specifications(lines: Lines) -> Instance:
    """
    Parse the problem specifications. These are lines that are formatted as
    KEY : VALUE.
    """
    data = {}

    for line in lines:
        if ": " in line:
            k, v = [x.strip() for x in re.split("\\s*: ", line, maxsplit=1)]
            data[k.lower()] = infer_type(v)

    return data


def parse_sections(lines: Lines) -> Instance:
    """
    Parse the sections data of the instance file. Sections start with a row
    containing NAME_SECTION followed by a number of lines with data.
    """
    name = None  # Used as key to store data
    sections = defaultdict(list)

    for line in lines:
        if "EOF" in line:
            break

        elif "_SECTION" in line:
            name = line.split("_SECTION")[0].strip()

        elif name is not None:
            row = [infer_type(num) for num in line.split()]

            # Most sections start with an index that we do not want to keep
            if name not in ["EDGE_WEIGHT", "DEPOT"]:
                row = row[1:]

            sections[name].append(row)

    data: Instance = {}

    for section_name, section_data in sections.items():
        section_name = section_name.lower()

        if section_name == "depot":
            depot_data = np.array(section_data)
            # TODO Keep this or remove?
            depot_data[:-1] -= 1  # Normalize depot indices to start at zero
            data[section_name] = depot_data
        elif section_name == "edge_weight":
            data[section_name] = section_data
        else:
            array = np.array(section_data)
            array = array.reshape(-1) if array.shape[1] == 1 else array

            data[section_name] = array

    return data


def parse_distances(instance: Instance, distance_rounding):
    """
    Creates the distances data.

    Using the specification "edge_weight_type" we can infer how to construct
    the distances: 1) either by computing the pairwise Euclidan distances
    using the provided coordinates or by 2) using the triangular matrix.
    """
    edge_weight_type = instance["edge_weight_type"]

    if "2D" in edge_weight_type:
        if callable(distance_rounding):  # custom rounding function
            round_func = distance_rounding
        elif edge_weight_type == "FLOOR_2D":
            round_func = math.floor
        elif edge_weight_type == "EXACT_2D":
            round_func = lambda n: n  # noqa
        elif edge_weight_type == "EUC_2D":
            round_func = round
        else:  # default is to round to nearest integer
            round_func = round

        return {"distances": euclidean(instance["node_coord"], round_func)}

    if edge_weight_type == "EXPLICIT":
        if instance["edge_weight_format"] == "LOWER_ROW":
            lr_repr = get_representation(
                instance["edge_weight"], n=instance["dimension"]
            )

            if lr_repr == "flattened":
                return {
                    "distances": from_flattened(
                        instance["edge_weight"], n=instance["dimension"]
                    )
                }

            elif lr_repr == "triangular":
                return {"distances": from_triangular(instance["edge_weight"])}


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
