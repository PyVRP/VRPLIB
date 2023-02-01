from typing import Any, Dict, Iterable

import numpy as np


def write_instance(path: str, **kwargs):
    """
    Writes a VRP instance to file following the VRPLIB format [1].

    Parameters
    ---------
    path
        The file path.
    **kwargs
        Optional keyword arguments. Each keyword-value pair is written to the
        instance file following convention:
        1) If `value` is a string, integer or float, then it is considered a
           problem specification and written as "{keyword}: {value}".
        2) If `value` is an n-by-m dimensional array, then it is considered a
           a data section and written as "{keyword}_SECTION" followed by `n`
           lines, each line containing the tab-separated `m` values.

        Otherwise, a ValueError is raised.

        # TODO I think

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


def write_section(fi, name: str, data: Iterable):
    """
    Writes a data section to file.

    A data section starts with the section name in all uppercase. It is then
    followed by row entries consisting of one or multiple values.
    """
    if name == "EDGE_WEIGHT":
        write_edge_weight_section(fi, data)
    elif name == "DEPOT":
        write_depot_section(fi, data)
    else:
        fi.write(f"{name}_SECTION\n")

        # TODO Refactor this
        if len(np.shape(data)) == 1:
            for idx, elt in enumerate(data, 1):
                row = f"{idx}\t{elt}"
                fi.write(row + "\n")
        else:
            for idx, elts in enumerate(data, 1):
                row = f"{idx}\t" + "\t".join(str(elt) for elt in elts)
                fi.write(row + "\n")


def write_edge_weight_section(fi, duration_matrix):
    """
    Writes the edge weight section. Rows do not start with index.
    """
    fi.write("EDGE_WEIGHT_SECTION\n")

    for row in duration_matrix:
        fi.write("\t".join(map(str, row)))
        fi.write("\n")


def write_depot_section(fi, depots):
    """
    Writes the depot section. Rows correspond to the index of the depot(s),
    where the final value is -1 to indicate termination.
    """
    fi.write("DEPOT_SECTION\n")

    for idx in depots:
        fi.write(f"{idx + 1}\n")

    fi.write("-1\n")
