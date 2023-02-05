# DEPRECATED
This package has been renamed. Use `pip install vrplib` instead.

# CVRPLIB
[![PyPI version](https://badge.fury.io/py/cvrplib.svg)](https://badge.fury.io/py/cvrplib)
[![cvrplib](https://github.com/leonlan/cvrplib/actions/workflows/cvrplib.yml/badge.svg)](https://github.com/leonlan/cvrplib/actions/workflows/cvrplib.yml)

This Python package provides functions to read and download instances from the Capacitated Vehicle Routing Problem Library ([CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/)). CVRPLIB contains a large collection of CVRP and VRPTW benchmark instances and also keeps track of the currently best known solutions.


# Installation
This library works with Python 3.7+.

```shell
pip install cvrplib
```


# Usage
Using this package is simple. We expose three functions:

-   `read`: Read an instance (and optionally solution) from a local file.
-   `download`: Download an instance (and optionally solution) directly from the CVRPLIB website.
-   `list_names`: List all instance names that can be passed to `download`.


## Example
```python
import cvrplib

# Read instances
instance = cvrplib.read('/path/to/A-n32-k5.vrp')
instance, solution = cvrplib.read(instance_path='/path/to/A-n32-k5.vrp',
                                  solution_path='/path/to/A-n32-k5.sol')

# Download instances
instance = cvrplib.download('A-n32-k5')
instance, solution = cvrplib.download('A-n32-k5', solution=True)

# List instance names 
cvrplib.list_names()                      # All instance names
cvrplib.list_names(low=100, high=200)     # Instances with between [100, 200] customers
cvrplib.list_names(vrp_type='vrptw')      # Only VRPTW instances
```
## Dataclasses
Instance fields depend on the VRP type of the instance. `Instance` defines the base instance, which is extended by the `CVRP` and `VRPTW` classes. `Solution` defines the solution and is the same for CVRP and VRPTW. 
```python
class Instance:
    name: str
    dimension: int
    n_customers: int
    depot: int
    customers: List[int]
    capacity: int
    distances: List[List[float]]
    demands: List[int]
    service_times: List[float]
    coordinates: Optional[List[List[float]]]

class CVRP(Instance):
    distance_limit: float

class VRPTW(Instance):
    n_vehicles: int
    earliest: List[int]
    latest: List[int]

class Solution:
    routes: List[int]
    cost: float
```

     
# Conventions
All instances are parsed according to the CVRPLIB convention. See Section 3.3 in [Uchoa et al. (2014)](http://www.optimization-online.org/DB_FILE/2014/10/4597.pdf) for more details. In short:
- The depot has index `0`. Customers are indexed from `1` to `n`.
- The distances are rounded to the nearest integer. 
    - Note that some benchmark sets were originally proposed without integer rounding. This is the case for the following sets: `CMT`, `Rochat and Taillard (tai)`, `Golden`, `Li`, `Solomon`, `Homberger and Gehring`.
    
# Remarks
- Downloading instances may take a few seconds. 
- The `XML100` benchmark set is not listed in `list_names` and cannot be downloaded using `download`. Please download these instances directly from [CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/) and use the `read` function instead.

    

