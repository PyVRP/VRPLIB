# VRPLIB
[![PyPI version](https://badge.fury.io/py/vrplib.svg)](https://badge.fury.io/py/vrplib)
[![vrplib](https://github.com/leonlan/vrplib/actions/workflows/vrplib.yaml/badge.svg)](https://github.com/leonlan/vrplib/actions/workflows/vrplib.yaml)
[![codecov](https://codecov.io/gh/leonlan/VRPLIB/branch/master/graph/badge.svg?token=X0X66LBNZ7)](https://codecov.io/gh/leonlan/VRPLIB)

`vrplib` is a Python package for reading Vehicle Routing Problem instances. It currently supports:
- reading VRPLIB and Solomon instances and solutions, and
- downloading instances and (best known) solutions from [CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/).

# Installation
This library works with Python 3.8+ and only depends on `numpy`. Install the latest version of `vrplib`:

```shell
pip install vrplib
```

# Example usage
## Reading instances and solutions
``` python
import vrplib

# Read VRPLIB formatted instances
instance = vrplib.read_instance("/path/to/X-n101-k25.vrp")
solution = vrplib.read_solution("/path/to/X-n101-k25.sol")

# Read Solomon formatted instances
instance = vrplib.read_instance("/path/to/C101.txt", instance_format="solomon")
solution = vrplib.read_solution("/path/to/C101.sol") 
```

## Downloading instances from CVRPLIB 
``` python
import vrplib

instance = vrplib.download_instance("X-n101-k25.vrp")
solution = vrplib.download_solution("X-n101-k25.sol")

# List instance names 
vrplib.list_names()                      # All instance names
vrplib.list_names(low=100, high=200)     # Instances with between [100, 200] customers
vrplib.list_names(vrp_type='cvrp')       # Only CVRP instances
vrplib.list_names(vrp_type='vrptw')      # Only VRPTW instances
```


# Documentation
Here we provide documentation for the `vrplib` library.

Philosophy: we parse an instance file as unopinionated as possible.
- If distances are given explicitly, then they are transformed into a full matrix if not already
- If distances are not explicitly provided, we parse them to be Euclidean and 2D without rounding as default
- If you dont want this, you can always change this.

# Conventions and terminology
   
# Remarks
- Downloading instances may take a few seconds. 
- The `XML100` benchmark set is not listed in `list_names` and cannot be downloaded through this package. You can download these instances directly from [CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/).

    
