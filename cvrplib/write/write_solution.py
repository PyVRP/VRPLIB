from typing import Dict, List, Union

Solution = Dict[str, Union[int, float, str, List[List[int]]]]


def write_solution(path: str, routes: List[List[int]], **kwargs):
    """
    Writes a VRP solution to file following the VRPLIB convention.

    Parameters
    ----------
    path
        The file path.
    routes
        A list of routes, each route denoting the order in which the customers
        are visited.
    **kwargs
        Optional keyword arguments. Each keyword-value pair is written to the
        solution file as "{keyword}: {value}".
    """
    with open(path, "w") as fi:
        for idx, route in enumerate(routes, 1):
            fi.write(f"Route #{idx}: {' '.join([str(s) for s in route])}")
            fi.write("\n")

        for k, v in kwargs.items():
            fi.write(f"{k}: {v}")
            fi.write("\n")
