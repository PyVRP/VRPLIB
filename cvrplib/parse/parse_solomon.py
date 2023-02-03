from typing import Dict, Union

import numpy as np

from .parse_distances import pairwise_euclidean
from .parse_utils import text2lines

Instance = Dict[str, Union[str, int, float, np.ndarray]]


def parse_solomon(text: str) -> Instance:
    """
    Parses the text of a Solomon VRPTW instance.

    Parameters
    ----------
    text
        The instance text.

    Returns
    -------
    The instance data as dictionary.
    """
    lines = text2lines(text)

    instance: Instance = {"name": lines[0]}
    instance["vehicles"], instance["capacity"] = [
        int(num) for num in lines[3].split()
    ]

    data = np.genfromtxt(lines[6:], dtype=int)

    instance["node_coord"] = data[:, 1:3]
    instance["demand"] = data[:, 3]
    instance["time_window"] = data[:, 4:6]
    instance["service_time"] = data[:, 6]
    instance["edge_weight"] = pairwise_euclidean(instance["node_coord"])

    return instance
