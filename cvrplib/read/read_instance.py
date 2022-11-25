from .parse_solomon import parse_solomon
from .parse_vrplib import parse_vrplib
from .utils import strip_lines


def read_instance(path, style="vrplib"):
    """
    Reads the instance from the passed-in file path.

    Parameters
    ----------
    path
        The file path.
    style
        The instance format style, one of ['vrplib', 'solomon'].

    Returns
    -------
    An dictionary that contains the instance data.
    """
    with open(path, "r") as fi:
        lines = strip_lines(fi)

        if style == "vrplib":
            return parse_vrplib(lines)
        elif style == "solomon":
            return parse_solomon(lines)

        raise ValueError(f"Format style {style} not known.")
