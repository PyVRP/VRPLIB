import numpy as np
from typing import Union, Optional

def parse_durations(
    data: list[list[float]],
    durations_weight_type: str = "EXPLICIT",  # Default to 'EXPLICIT'
    durations_weight_format: Optional[str] = "FULL_MATRIX",  # Default to 'FULL_MATRIX'
    **kwargs: Union[float, str, np.ndarray],  # Optional keyword arguments
) -> np.ndarray:
    """
    Parses the duration matrix based on the specified durations_weight_type.
    Currently, only the 'FULL_MATRIX' format is supported.

    Parameters
    ----------
    data : list of lists
        The duration data as a list of lists, representing a full matrix.
    durations_weight_type : str, optional
        The type of duration weight, defaults to 'EXPLICIT'.
    durations_weight_format : str, optional
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
        If the durations_weight_type or durations_weight_format is unsupported.
    """
    if durations_weight_type == "EXPLICIT" and durations_weight_format == "FULL_MATRIX":
        return np.array(data)
    
    raise ValueError(f"Unsupported durations_weight_type: {durations_weight_type} or format: {durations_weight_format}.")
