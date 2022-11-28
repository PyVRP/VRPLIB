from typing import Dict, List, Union

from .utils import infer_type

SolutionData = Union[int, float, str, List]


def parse_solution(lines: List[str]) -> Dict[str, SolutionData]:
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
    data: Dict[str, SolutionData] = {"routes": []}

    for line in lines:
        line = line.strip().lower()

        if "route" in line:
            route = [int(idx) for idx in line.split(":")[1].split(" ") if idx]
            data["routes"].append(route)  # type:ignore
        elif ":" in line or " " in line:  # split at first colon or whitespace
            split_at = ":" if ":" in line else " "
            k, v = [word.strip() for word in line.split(split_at, 1)]
            data[k] = infer_type(v)
        else:  # ignore non keyword-value pairs
            continue

    return data
