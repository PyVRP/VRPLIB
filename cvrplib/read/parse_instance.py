from .cvrp import parse_cvrp
from .vrptw import parse_vrptw


def parse_instance(lines, style="vrplib"):
    """
    Parse the passed-in lines and return the corresponding instance.
    """
    if style == "vrplib":
        instance = parse_cvrp(lines)
    elif style == "solomon":
        instance = parse_vrptw(lines)
    else:
        raise ValueError("Style {style} not known.")

    return instance


def is_vrptw(set_name: str) -> bool:
    """
    Checks if the set name belongs to VRPTW; otherwise it belons to CVRP.
    """
    # TODO This is not a foolproof way to differentiate between CVRP and VRPTW
    return set_name in ["HG", "Solomon"]
