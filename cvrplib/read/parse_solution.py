from typing import Dict, List, Union


def parse_solution(lines: List[str]) -> Dict[str, Union[List, float]]:
    """
    Parses the text of a solution file formatted in VRPLIB style. A solution
    consists of routes, which are indexed from 1 to n, and possibly other data.

    Parameters
    ----------
    lines
        The lines of a solution text file.

    Returns
    -------
    A dictionary that contains solution data.

    """
    data: Dict[str, Union[List, float]] = {}

    routes = []

    for line in lines:
        line = line.strip().lower()

        if not line.startswith("route"):
            continue

        route = [int(cust) for cust in line.split(":")[1].split(" ") if cust]
        routes.append(route)

    data["routes"] = routes

    # Find the cost
    for line in lines:
        line = line.strip().lower()

        if "cost" in line:
            cost = line.lstrip("cost ")
            data["cost"] = int(cost) if cost.isdigit() else float(cost)
            break

    return data
