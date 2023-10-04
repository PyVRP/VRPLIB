from pathlib import Path
from typing import Union

import numpy as np


def write_instance(
    path: Union[str, Path],
    data: dict[str, Union[str, float, list, np.ndarray]],
):
    """
    Writes a VRP instance to file following the VRPLIB format [1].

    Parameters
    ---------
    path
        The file path.
    data
        A dictionary of keyword-value pairs. For each key-value pair, the
        following rules apply:
        * If ``value`` is a string, integer or float, then it is considered a
          problem specification and written as "{keyword}: {value}".
        * If ``value`` is a list or numpy array, then it is considered a
          data section and formatted as
          ```
          {name}
          1 {row_1}
          2 {row_2}
          ...
          n {row_n}
          ```
          where ``name`` is the key and ``row_1``, ``row_2``, etc. are the
          elements of the array. If name is "EDGE_WEIGHT_SECTION" or
          "DEPOT_SECTION", then the index is not included.


    References
    ----------
    [1] Helsgaun, K. (2017). An Extension of the Lin-Kernighan-Helsgaun TSP
        Solver for Constrained Traveling Salesman and Vehicle Routing
        Problems.
        http://webhotel4.ruc.dk/~keld/research/LKH-3/LKH-3_REPORT.pdf

    """
    with open(path, "w") as fh:
        for key, value in data.items():
            if isinstance(value, (np.ndarray, list)):
                fh.write(_format2section(key, value))
            else:
                fh.write(f"{key}: {value}" + "\n")

        fh.write("EOF\n")


def _format2section(
    name: str, data: Union[list, list[list], np.ndarray]
) -> str:
    text = f"{name}\n"

    # Convert the data to a 2-dimensional numpy array.
    array = np.asarray(data)
    if array.ndim == 1:
        array = np.expand_dims(array, axis=1)

    # These lengths are used to space each column properly.
    lens = [4 for _ in range(len(array[0]) + 1)]

    for row in array:
        for idx, cell in enumerate(row, 1):
            lens[0] = max(lens[0], len(str(idx)))
            lens[idx] = max(lens[idx], len(str(cell)))

    for idx, row in enumerate(array, 1):
        if name not in ["EDGE_WEIGHT_SECTION", "DEPOT_SECTION"]:
            text += str(idx)  # include index if not edge weight or depot

        text += "  ".join(f"{val:>{ln}}" for ln, val in zip(lens, row)) + "\n"

    return text
