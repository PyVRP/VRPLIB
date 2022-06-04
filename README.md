# pyCVRPLIB
[![PyPI version](https://badge.fury.io/py/pycvrplib.svg)](https://badge.fury.io/py/pycvrplib)
[![pyCVRPLIB](https://github.com/leonlan/pyCVRPLIB/actions/workflows/pycvrplib.yml/badge.svg)](https://github.com/leonlan/pyCVRPLIB/actions/workflows/pycvrplib.yml)

This Python package provides functions to read and download instances from the Capacitated Vehicle Routing Problem Library ([CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/)), which contains a large collection of CVRP instances and also keeps track of the currently best known solutions.

This package is inspired by [CVRPLIB.jl](https://github.com/chkwon/CVRPLIB.jl).


<a id="org6ad8585"></a>

# Installation

This library works with Python 3.7+.

```shell
pip install pycvrplib
```


<a id="org5b103be"></a>

# Usage

Using this package is simple, it exposes the following three functions:
-   `read`: Return an instance (and optionally solution) by reading a local file.
-   `download`: Return an instance (and optionally solution) by directly downloading it from the CVRPLIB website using the corresponding set and instance name.
-   `list_instances`: Return a list of all instance names that can be passed to `download`. Includes the set names.


<a id="org9003630"></a>

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

<a id="org50088b2"></a>

# Conventions

-   The depot has index `0`, whereas customers are indexed from `1` to `n`.
-   The distances are all assumed to be integral, where instances calculated by taking the Euclidean distance are rounded to the nearest integer. Note that some of the reported best known solutions have non-rounded distances and are thus floating point numbers. This is the case for the following data sets: `CMT`, `Rochat and Taillard`, `Golden`, `Li`, `Solomon`, `Homberger and Gehring`.


<a id="org90b4a50"></a>

# Remarks

-   Downloading and listing instances may take a while (a few seconds). Please let me know if you know how to fix this.
-   The `XML100` data set, which contains 10000 CVRP instances for training ML algorithms, is not listed in `list_instances` and cannot be downloaded using the `download` function. Please download these instances directly from [CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/). This package does support reading the instances.
-   Our package currently does not support reading and downloading VRPTW instances, i.e., instances that belong to the `Solomon` and `Homberger and Gehring` set. Support for this will be in a later version.

