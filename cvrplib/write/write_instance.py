from typing import Any, Dict, Iterable

import numpy as np


def write_instance(path: str, instance: Dict[str, Any]):
    """
    Write a VRP instance to file following the LKH-3 VRPLIB format [1].

    path
        The path of the file.
    instance
        The instance dictionary, containing problem specifications and data.

    References
    ----------
    .. [1] Helsgaun, K. (2017). An Extension of the Lin-Kernighan-Helsgaun TSP
           Solver for Constrained Traveling Salesman and Vehicle Routing
           Problems.
           http://webhotel4.ruc.dk/~keld/research/LKH-3/LKH-3_REPORT.pdf

    """
    with open(path, "w") as fi:
        for k, v in instance.items():
            if isinstance(v, (np.ndarray, list)):
                write_section(fi, k.upper(), v)
            else:
                fi.write(f"{k.upper()} : {v}")
                fi.write("\n")

        fi.write("EOF\n")


def write_section(f, name: str, data: Iterable):
    """
    Write a data section to file. A data section starts with the section name
    in all uppercase. It is then followed by rows corresponding to the data
    entries. Each row starts with the index (starting at 1) and the data
    elements are separated by tabs.
    """
    # Sections that have a different format
    if name == "EDGE_WEIGHT":
        write_edge_weight_section(f, data)
    elif name == "DEPOT":
        write_depot_section(f, data)
    else:
        f.write(f"{name}_SECTION\n")

        # TODO Refactor this
        if len(np.shape(data)) == 1:
            for idx, elt in enumerate(data, 1):
                row = f"{idx}\t{elt}"
                f.write(row + "\n")
        else:
            for idx, elts in enumerate(data, 1):
                row = f"{idx}\t" + "\t".join(str(elt) for elt in elts)
                f.write(row + "\n")


def write_edge_weight_section(f, duration_matrix):
    f.write("EDGE_WEIGHT_SECTION\n")

    for row in duration_matrix:
        f.write("\t".join(map(str, row)))
        f.write("\n")


def write_depot_section(f, depots):
    f.write("DEPOT_SECTION\n")

    for idx in depots[:-1].flatten():
        f.write(f"{idx + 1}\n")

    f.write("-1\n")  # terminate section
