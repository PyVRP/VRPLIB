from vrplib.parse import parse_solution


def read_solution(path: str):
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
