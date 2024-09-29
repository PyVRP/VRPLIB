import numpy as np

def parse_durations(
    data: list[list[float]],
) -> np.ndarray:
    """
    Parses the duration matrix, assuming the full matrix format.

    Parameters
    ----------
    data
        The duration data as a list of lists, representing a full matrix.

    Returns
    -------
    np.ndarray
        A numpy array representing the duration matrix.
    """
    # Convert the list of lists to a numpy array
    return np.array(data)
