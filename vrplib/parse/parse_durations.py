import numpy as np
from typing import Union, Optional

def parse_durations(
    data: list[list[float]],
    edge_duration_type: str = "EXPLICIT",  # Default to 'EXPLICIT'
    edge_duration_format: Optional[str] = "FULL_MATRIX",  # Default to 'FULL_MATRIX'
    **kwargs: Union[float, str, np.ndarray],  # Optional keyword arguments
) -> np.ndarray:
    """
    Parses the duration matrix based on the specified edge_duration_type.
    Currently, only the 'FULL_MATRIX' format is supported.

    Parameters
    ----------
    data : list of lists
        The duration data as a list of lists, representing a full matrix.
    edge_durations_type : str, optional
        The type of duration weight, defaults to 'EXPLICIT'.
    edge_duration_format : str, optional
        The format of the duration weights, defaults to 'FULL_MATRIX'.
    **kwargs : dict, optional
        Optional keyword arguments for additional parameters.

    Returns
    -------
    np.ndarray
        A numpy array representing the duration matrix.

    Raises
    ------
    ValueError
        If the edge_durations_type or edge_duration_format is unsupported.
    """
    if edge_duration_type == "EXPLICIT" and edge_duration_format == "FULL_MATRIX":
        return np.array(data)
    
    raise ValueError(f"Unsupported durations_weight_type: {edge_duration_type} or format: {edge_duration_format}.")