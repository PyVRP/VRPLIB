import os
from typing import Any, Dict, Union

from vrplib.parse import parse_solomon, parse_vrplib


def read_instance(
    path: Union[str, os.PathLike],
    instance_format: str = "vrplib",
    compute_edge_weights: bool = True,
) -> Dict[str, Any]:
    """
    Reads the instance from the passed-in file path.

    Parameters
    ----------
    path
        The path to the instance file.
    instance_format
        The instance format, one of ["vrplib", "solomon"]. Default is "vrplib".
    compute_edge_weights
        Whether to calculate edge weights based on instance specifications
        and node coordinates, if not explicitly provided. Defaults to True.

    Returns
    -------
    A dictionary that contains the instance data.
    """
    with open(path, "r") as fi:
        if instance_format == "vrplib":
            return parse_vrplib(fi.read(), compute_edge_weights)
        elif instance_format == "solomon":
            return parse_solomon(fi.read(), compute_edge_weights)

        raise ValueError(f"Format style {instance_format} not known.")
