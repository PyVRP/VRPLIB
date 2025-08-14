import os
from typing import TypeVar

import numpy as np

_ArrayLike = TypeVar("_ArrayLike", list, tuple, np.ndarray)


def write_instance(
    path: str | os.PathLike,
    data: dict[str, str | int | float | _ArrayLike],
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
          problem specification and formatted as "{keyword}: {value}".
        * If ``value`` is a one or two-dimensional array, then it is considered
          a data section and formatted as
          ```
          {name}
          1 {row_1}
          2 {row_2}
          ...
          n {row_n}
          ```
          where ``name`` is the key and ``row_1``, ``row_2``, etc. are the
          elements of the array. One-dimensional arrays are treated as column
          vectors. If name is "EDGE_WEIGHT_SECTION" or "DEPOT_SECTION", then
          the index is not included.

    References
    ----------
    [1] Helsgaun, K. (2017). An Extension of the Lin-Kernighan-Helsgaun TSP
        Solver for Constrained Traveling Salesman and Vehicle Routing
        Problems.
        http://webhotel4.ruc.dk/~keld/research/LKH-3/LKH-3_REPORT.pdf

    """
    with open(path, "w") as fh:
        for key, value in data.items():
            if isinstance(value, (str, int, float)):
                fh.write(f"{key}: {value}" + "\n")
            else:
                fh.write(_format_section(key, value) + "\n")

        fh.write("EOF\n")


def _format_section(name: str, data: _ArrayLike) -> str:
    """
    Formats a data section.

    Parameters
    ----------
    name
        The name of the section.
    data
        The data to be formatted.

    Returns
    -------
    str
        A VRPLIB-formatted data section.
    """
    section = [name]
    include_idx = name not in ["EDGE_WEIGHT_SECTION", "DEPOT_SECTION"]

    if _is_one_dimensional(data):
        # Treat 1D arrays as column vectors, so each element is a row.
        for idx, elt in enumerate(data, 1):
            prefix = f"{idx}\t" if include_idx else ""
            section.append(prefix + str(elt))
    else:
        for idx, row in enumerate(data, 1):
            prefix = f"{idx}\t" if include_idx else ""
            rest = "\t".join([str(elt) for elt in row])
            section.append(prefix + rest)

    return "\n".join(section)


def _is_one_dimensional(data: _ArrayLike) -> bool:
    return all(not isinstance(elt, (list, tuple, np.ndarray)) for elt in data)
