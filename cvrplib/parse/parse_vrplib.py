import re
from collections import defaultdict
from typing import Any, Dict, List

import numpy as np

from .parse_distances import parse_distances
from .parse_utils import infer_type, text2lines

Instance = Dict[str, Any]
Lines = List[str]


def parse_vrplib(text: str, distance_rounding=None):
    """
    Parses the instance text. An instance consists of two main parts:
    - Problem specifications [name, dimension, edge_weight_type, ...]
    - Data sections [node coords, demands, time windows, ...]

    Parameters
    ----------
    text
        The instance text.
    distance_rounding
        An optional function for custom distance rounding.
    """
    lines = text2lines(text)
    instance = parse_lines(lines)

    # We post-process distances (e.g., compute Euclidean distances from coords,
    # or create a full matrix from an upper-triangular one).
    distances = parse_distances(instance, distance_rounding)
    instance.update(distances if distances else {})

    return instance


def parse_lines(lines: Lines) -> Instance:
    data = {}
    sections = defaultdict(list)
    name = None  # Used as key to store section data

    for line in lines:
        if "EOF" in line:
            break

        if ": " in line:
            k, v = [x.strip() for x in re.split("\\s*: ", line, maxsplit=1)]
            data[k.lower()] = infer_type(v)

        elif "_SECTION" in line:
            name = line.split("_SECTION")[0].strip()

        elif name is not None:
            row = [infer_type(num) for num in line.split()]

            # Most sections start with an index that we do not want to keep
            if name not in ["EDGE_WEIGHT", "DEPOT"]:
                row = row[1:]

            sections[name].append(row)

    # Parse the sections separately to deal with
    for section_name, section_data in sections.items():
        section_name = section_name.lower()

        if section_name == "depot":
            depot_data = np.array(section_data)
            # TODO Keep this convention of keep the original indices?
            depot_data[:-1] -= 1  # Normalize depot indices to start at zero
            data[section_name] = depot_data
        elif section_name == "edge_weight":
            data[section_name] = section_data
        else:
            array = np.array(section_data)
            array = array.reshape(-1) if array.shape[1] == 1 else array

            data[section_name] = array

    return data
