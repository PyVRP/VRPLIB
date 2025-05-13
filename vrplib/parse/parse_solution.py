from typing import Union

from .parse_utils import infer_type, text2lines

Solution = dict[str, Union[float, str, list]]


def parse_solution(text: str) -> Solution:
    """
    Parses a VRPLIB-formatted solution text into a dictionary.
    - Routes appear as "Route #n: node1 node2 node3..." where nodes can be:
      * Integer indices (0-indexed, unlike 1-indexed instance data)
      * String markers (e.g., "|" for reload depots).
    - Additional metadata as key-value pairs (e.g., "Cost: 123.45")

    Parameters
    ----------
    text
        The solution text.

    Returns
    -------
    dict
        The soluion data dictionary, containing:
        - "routes": list of routes, each route being a list of nodes
        - Additional metadata as key-value pairs from the solution
    """
    solution: Solution = {"routes": []}

    for line in text2lines(text):
        if "Route" in line:
            raw_visits = line.split(":")[1].split()
            visits = [int(val) if val.isdigit() else val for val in raw_visits]
            solution["routes"].append(visits)  # type: ignore
        elif ":" in line or " " in line:  # Split at first colon or whitespace
            split_at = ":" if ":" in line else " "
            k, v = [word.strip() for word in line.split(split_at, 1)]
            solution[k.lower()] = infer_type(v)
        else:  # Ignore lines without keyword-value pairs
            continue

    return solution
