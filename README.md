# pyCVRPLIB
[![PyPI version](https://badge.fury.io/py/pycvrplib.svg)](https://badge.fury.io/py/pycvrplib)
[![pyCVRPLIB](https://github.com/leonlan/pyCVRPLIB/actions/workflows/pycvrplib.yml/badge.svg)](https://github.com/leonlan/pyCVRPLIB/actions/workflows/pycvrplib.yml)

This Python package provides functions to read and download instances from the Capacitated Vehicle Routing Problem Library ([CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/)). CVRPLIB contains a large collection of CVRP and VRPTW benchmark instances and also keeps track of the currently best known solutions.


# Installation

This library works with Python 3.7+ and be installed using

```shell
pip install pycvrplib
```


# Usage

Using this package is simple. We expose three functions:

-   **`read`:** Read an instance (and optionally solution) from a local file.
-   **`download`:** Download an instance (and optionally solution) directly from the CVRPLIB website.
-   **`list_instances`:** Return a list of all instance names that can be passed to `download`. Includes the set names.


## Example
```python
import pycvrplib

# Read instances
instance = pycvrplib.read('/path/to/A-n32-k5.vrp')
instance, solution = pycvrplib.read(instance_path='/path/to/A-n32-k5.vrp',
                                    solution_path='/path/to/A-n32-k5.sol')

# List all instance names including set name
pycvrplib.list_instances()

# To directly download an instance and the corresponding solution, you must
# provide the instance name prefixed with the corresponding set name and a
# forward slash. For example, the =A-n32-k5= instance belongs to the set =A=,
# hence =A/A-n32-k5= is the correct name to download this instance.

# Note that downloading may take a few seconds.
instance = pycvrplib.download('A/A-n32-k5')
instance, solution = pycvrplib.download('A/A-n32-k5', solution=True)
```
The `instance` and `solution` objects are defined by their respective classes as follows:
```python
@dataclass
class Instance:
    name: str
    comment: str
    dimension: int
    capacity: int
    distances: List[List[float]]
    demands: List[int]
    depot: int
    coordinates: Optional[List[List[float]]] = None

@dataclass
class Solution:
    routes: List[int]
    cost: float
```


# Conventions
-   The depot has index `0`, whereas customers are indexed from `1` to `n`.
-   The distances are all assumed to be integral, where instances calculated by taking the Euclidean distance are rounded to the nearest integer. Note that some of the reported best known solutions have non-rounded distances and are thus the best known solution costs are represented by floats. This is the case for the following sets: `CMT`, `Rochat and Taillard`, `Golden`, `Li`, `Solomon`, `Homberger and Gehring`.

# Remarks
-   Downloading instances may take a few seconds. 
-   The `XML100` data set, which contains 10000 CVRP instances for training ML algorithms, is not listed in `list_instances` and cannot be downloaded using the `download` function. Please download these instances directly from [CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/). This package does support reading the instances.

