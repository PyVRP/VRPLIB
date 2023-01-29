from typing import Callable, Dict, Optional, Union, no_type_check

import numpy as np

from .parse_distances import euclidean
from .parse_utils import text2lines

Instance = Dict[str, Union[str, int, float, np.ndarray]]


@no_type_check
def parse_solomon(
    text: str, distance_rounding: Optional[Callable] = None
) -> Instance:
    """
    Parses the content of a Solomon VRPTW instance.

    A Solomon-type instance consists of a vehicle data section and a customer
    data section. The vehicle section starts with line containing "VEHICLE".
    The second line contains the words "NUMBER" and "CAPACITY", meaning the
    number of vehicles and the vehicle capacity, repsectively. The third line
    specifies an integer value for the vehicle number and vehicle capacity.

    The customer section starts with a line containing "CUSTOMER". The second
    line should specify the customer field names. It is followed by a new line.
    The remaining lines contain the data for each customer.

    # TODO should the distance be provided or not?

    Parameters
    ----------
    text
        The instance text.
    distance_rounding
        A custom distance rounding function.
    """
    lines = text2lines(text)

    instance: Instance = {"name": lines[0]}
    instance["vehicle_number"], instance["vehicle_capacity"] = [
        int(num) for num in lines[3].split()
    ]

    data = np.genfromtxt(lines[6:], dtype=int)

    instance["cust_no"] = data[:, 0]
    instance["xcoord"] = data[:, 1]
    instance["ycoord"] = data[:, 2]
    instance["demand"] = data[:, 3]
    instance["ready_time"] = data[:, 4]
    instance["due_date"] = data[:, 5]
    instance["service_time"] = data[:, 6]
    instance["distances"] = euclidean(
        np.column_stack([instance["xcoord"], instance["ycoord"]]),
        distance_rounding if distance_rounding is not None else _identity,
    )

    return instance


def _identity(x):
    return x
