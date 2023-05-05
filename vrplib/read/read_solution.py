import os
from typing import Union

from vrplib.parse import parse_solution
from vrplib.Solution import Solution


def read_solution(path: Union[str, os.PathLike]) -> Solution:
    """
    Reads the solution from the passed-in file path.

    Parameters
    ----------
    path
        The path to the solution file.

    Returns
    -------
    A dictionary that contains the solution data.

    """
    with open(path, "r") as fi:
        return parse_solution(fi.read())
