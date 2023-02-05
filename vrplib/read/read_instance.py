from vrplib.parse import parse_solomon, parse_vrplib


def read_instance(path, instance_format="vrplib"):
    """
    Reads the instance from the passed-in file path.

    Parameters
    ----------
    path
        The path to the instance file.
    style
        The instance format, one of ['vrplib', 'solomon'].

    Returns
    -------
    dict
        The instance data.
    """
    with open(path, "r") as fi:
        if instance_format == "vrplib":
            return parse_vrplib(fi.read())
        elif instance_format == "solomon":
            return parse_solomon(fi.read())

        raise ValueError(f"Format style {instance_format} not known.")
