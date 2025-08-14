import os
from typing import Any


def write_solution(
    path: str | os.PathLike,
    routes: list[list[int]],
    data: dict[str, Any] | None = None,
):
    """
    Writes a VRP solution to file following the VRPLIB convention.

    Parameters
    ----------
    path
        The file path.
    routes
        A list of routes, each route denoting the order in which the customers
        are visited.
    data
        Optional data dictionary. Each key-value pair is written to the
        solution file as "{key}: {value}".
    """
    for route in routes:
        if len(route) == 0:
            raise ValueError("Empty route in solution.")

    with open(path, "w") as fi:
        for idx, route in enumerate(routes, 1):
            text = " ".join([f"Route #{idx}:"] + [str(val) for val in route])
            fi.write(text + "\n")

        if data is not None:
            for key, value in data.items():
                fi.write(f"{key}: {value}\n")
