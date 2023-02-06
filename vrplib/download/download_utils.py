import re

from .constants import CVRP_SETS, DIMACS_NAMES, XXL_NAMES


def find_set(instance_name: str) -> str:
    """
    Find the set name of the instance.

    Notes
    -----
    - VRPTW instances start with "C, R, RC" directly followed by 1 or 2.
        HG instances have underscores ("_") in the name, whereas Solomon
        instances do not.
    - CVRP instance names and their corresponding set names share the same
        first letter. the exceptions are XXL and DIMACS instances, which have
        unique instance names
    """
    if re.match("(R|C|RC)[12]", instance_name):
        if "_" in instance_name:
            return "HG"
        else:
            return "Solomon"

    if any([instance_name.startswith(xxl) for xxl in XXL_NAMES]):
        return "XXL"

    if any([instance_name.startswith(dimacs) for dimacs in DIMACS_NAMES]):
        return "D"

    for set_name in CVRP_SETS:
        if instance_name.startswith(set_name):
            return set_name

    raise ValueError(f"Set name not known for instance: {instance_name}.")


def is_vrptw(name: str) -> bool:
    """
    Checks if the passed-in name is a VRPTW instance or not. Otherwise the
    instance is a CVRP instance.
    """
    return find_set(name) in ["HG", "Solomon"]
