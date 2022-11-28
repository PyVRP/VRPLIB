from typing import Dict, List, Union

from .parse_utils import infer_type, text2lines

Solution = Dict[str, Union[int, float, str, List]]


def parse_solution(text: str) -> Solution:
    """
    Parses the text of a solution file formatted in VRPLIB style. A solution
    consists of routes, which are indexed from 1 to n, and possibly other data.

    Parameters
    ----------
    text
        The solution text.

    Returns
    -------
    A dictionary that contains solution data.
    """
    lines = text2lines(text)

    solution: Solution = {"routes": []}

    for line in lines:
        line = line.lower()

        if "route" in line:
            route = [int(idx) for idx in line.split(":")[1].split(" ") if idx]
            solution["routes"].append(route)  # type: ignore
        elif ":" in line or " " in line:  # Split at first colon or whitespace
            split_at = ":" if ":" in line else " "
            k, v = [word.strip() for word in line.split(split_at, 1)]
            solution[k] = infer_type(v)
        else:  # Ignore lines without keyword-value pairs
            continue

    return solution
