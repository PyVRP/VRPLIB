# VRPLIB
[![PyPI version](https://badge.fury.io/py/vrplib.svg)](https://badge.fury.io/py/vrplib)
[![vrplib](https://github.com/leonlan/vrplib/actions/workflows/vrplib.yaml/badge.svg)](https://github.com/leonlan/vrplib/actions/workflows/vrplib.yaml)
[![codecov](https://codecov.io/gh/leonlan/VRPLIB/branch/master/graph/badge.svg?token=X0X66LBNZ7)](https://codecov.io/gh/leonlan/VRPLIB)

`vrplib` is a Python package for reading Vehicle Routing Problem (VRP) instances. The main features are:
- reading VRPLIB and Solomon instances and solutions, and
- downloading instances and best known solutions from [CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/).

# Installation
This library works with Python 3.8+ and only depends on `numpy`. Install the latest version of `vrplib`:

```shell
pip install vrplib
```

# Example usage
## Reading instances and solutions
```python
import vrplib

# Read VRPLIB formatted instances (default)
instance = vrplib.read_instance("/path/to/X-n101-k25.vrp")
solution = vrplib.read_solution("/path/to/X-n101-k25.sol")

# Read Solomon formatted instances
instance = vrplib.read_instance("/path/to/C101.txt", instance_format="solomon")
solution = vrplib.read_solution("/path/to/C101.sol") # only 1 solution format
```

`instance` and `solution` are dictionaries that contain all parsed data. 
``` python
instance.keys()
# dict_keys(['name', 'comment', 'type', 'dimension', ..., 'edge_weight'])

solutions.keys()
# dict_keys(['routes', 'cost'])
```


## Downloading instances from CVRPLIB 
``` python
import vrplib

instance = vrplib.download_instance("X-n101-k25.vrp")
solution = vrplib.download_solution("X-n101-k25.sol")

# List instance names that can be downloaded 
vrplib.list_names()                      # All instance names
vrplib.list_names(low=100, high=200)     # Instances with between [100, 200] customers
vrplib.list_names(vrp_type='cvrp')       # Only CVRP instances
vrplib.list_names(vrp_type='vrptw')      # Only VRPTW instances
```


# Notes
This section contains additional notes about the `vrplib` package.

## Instance formats
Currently, two VRP instance formats are supported:
- **VRPLIB**: this format is most commonly used for Capacitated Vehicle Routing Problem (CVRP) instances.  See the [X-n101-k25](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/X/X-n101-k25.vrp) instance for an example. VRPLIB is an extension of the [TSPLIB95](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf) format. Additional information about the VRPLIB format can be found [here]( http://webhotel4.ruc.dk/~keld/research/LKH-3/LKH-3_REPORT.pdf). 
- **Solomon**: this format was used to introduce the Solomon instances for the Vehicle Routing Problem with Time Window (VRPTW) and also the extended instance set by Homberger and Gehring. See the [C101](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/Solomon/C101.txt) instance for an example.

## How instances are parsed
`vrplib` parses an instance and returns a dictionary of keyword-value pairs. There are two types of instance data: 
- Problem specifications, which may contain metadata or problem-specific information such as the max number of vehicles. 
- Problem data, which are often arrays of values describing, for example, customer service times and time windows. 

### On parsing distances 
The `vrplib` library tries to follow the instance specifications as strictly as possible to compute the distances. 

For VRPLIB instances, the distances computation is determined by the `EDGE_WEIGHT_TYPE` and possibly the `EDGE_WEIGHT_FORMAT` specifications. We currently support two categories of edge weight types:
- `*_2D`: compute the Euclidean distances using the node coordinate data.
    - `EUC_2D`: Double precision distances without rounding.
    - `FLOOR_2D`: Round down all distances to down to an integer.
    - `EXACT_2D`: Multiply the distances by 1000, round to the nearest integer.
- `EXPLICIT`: the distance data is explicitly provided, in partial or full form. For explicit matrices, the `EDGE_WEIGHT_FORMAT` must be specified. We support the following two formats:
  - `LOWER_ROW`: Lower row triangular matrix without diagonal entries.  
  - `FULL_MATRIX`: Explicit full matrix representation.
  
More information about how VRPLIB specifications can be found [here](  http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf) and [here]( http://webhotel4.ruc.dk/~keld/research/LKH-3/LKH-3_REPORT.pdf).

Note that there are VRPLIB instances that use different rounding conventions in the literature, which may not be specified in the instance. For example, the X instance set proposed by [Uchoa et al. (2017)](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/new-instances) assumes that the distances are rounded to the nearest integer. When you use the `vrplib` package to read instances from the X set, it will return unrounded Euclidean distances because the instance specifies the `EUC_2D` edge weight type, i.e., no rouding. This can be easily solved by rounding the distances matrix manually.

For Solomon-type instances, the distance computation is not specified in the instance file, hence we compute the Euclidean distances without rounding. A recent convention that was proposed during the [2021 DIMACS Vehicle Routing Implementation Challenge](http://dimacs.rutgers.edu/programs/challenge/vrp/vrptw/) is to truncate the Euclidean distances to one decimal. Similar to the X instance set, you can manually modify the distances matrix.

## Additional remarks
- Downloading instances may take up to a few seconds. 
- The `XML100` benchmark set is not listed in `list_names` and cannot be downloaded through this package. You can download these instances directly from [CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/).

    
