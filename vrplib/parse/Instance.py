from typing import TypedDict, Union

import numpy as np


class Instance(TypedDict, total=False):
    # Specifications
    name: str
    dimension: int  # number of depots + number of customers
    edge_weight_format: str
    edge_weight_type: str
    display_type: str
    comment: str
    vehicles: int  # number of vehicles
    capacity: int

    # Data sections
    node_coord: np.ndarray
    demand: np.ndarray
    depot: Union[np.ndarray]
    service_time: np.ndarray
    time_window: np.ndarray
    edge_weight: np.ndarray
