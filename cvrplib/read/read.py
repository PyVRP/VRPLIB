import warnings
from typing import Optional

from .read_instance import read_instance
from .read_solution import read_solution


def read(instance_path: str, solution_path: Optional[str] = None):
    """
    Reads the instance (and optionally the solution) from the provided paths.
    """
    message = (
        "cvrplib.read has been deprecated in favor of cvrplib.read_instance "
        "and cvrplib.read_solution."
    )
    warnings.warn(message, DeprecationWarning, stacklevel=2)

    # NOTE We assume here that the file names are unmodified w.r.t. to CVPRLIB,
    # so this does not work when the file names are changed. But since this
    # function is deprecated there is no reason to change this.
    style = "solomon" if ".txt" in str(instance_path) else "vrplib"

    instance = read_instance(instance_path, style=style)

    if solution_path is None:
        return instance

    return instance, read_solution(solution_path)
