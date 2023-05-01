from vrplib.parse import parse_solomon, parse_vrplib


def read_instance(path, instance_format="vrplib", compute_edge_weights=True):
    """
    Reads the instance from the passed-in file path.

    Parameters
    ----------
    path
        The path to the instance file.
    instance_format
        The instance format, one of ['vrplib', 'solomon'].
    compute_edge_weights
        Whether to compute the edge weights. Default is True.

    Returns
    -------
    dict
        The instance data.
    """
    with open(path, "r") as fi:
        if instance_format == "vrplib":
            return parse_vrplib(fi.read(), compute_edge_weights)
        elif instance_format == "solomon":
            return parse_solomon(fi.read(), compute_edge_weights)

        raise ValueError(f"Format style {instance_format} not known.")
