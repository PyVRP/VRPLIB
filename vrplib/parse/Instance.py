from typing import TypedDict

import numpy as np


class Instance(TypedDict, total=False):
    # Specifications
    name: str
    edge_weight_format: str
    edge_weight_type: str
    comment: str
    vehicles: int  # number of vehicles
    capacity: int

    # Data sections
    node_coord: np.ndarray
    demand: np.ndarray
    depot: int | np.ndarray
    service_time: np.ndarray
    time_window: np.ndarray
    edge_weight: np.ndarray
