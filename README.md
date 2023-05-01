# VRPLIB
[![PyPI version](https://badge.fury.io/py/vrplib.svg)](https://badge.fury.io/py/vrplib)
[![vrplib](https://github.com/leonlan/vrplib/actions/workflows/vrplib.yaml/badge.svg)](https://github.com/leonlan/vrplib/actions/workflows/vrplib.yaml)
[![codecov](https://codecov.io/gh/leonlan/VRPLIB/branch/master/graph/badge.svg?token=X0X66LBNZ7)](https://codecov.io/gh/leonlan/VRPLIB)

`vrplib` is a Python package for reading Vehicle Routing Problem (VRP) instances. The main features are:
- reading VRPLIB and Solomon instances and solutions, and
- downloading instances and best known solutions from [CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/).

## Installation
This library works with Python 3.8+ and only depends on `numpy`. Install the latest version of `vrplib`:

```shell
pip install vrplib
```

## Example usage
### Reading instances and solutions
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


### Downloading instances from CVRPLIB 
``` python
import vrplib

# Download an instance and a solution file
vrplib.download_instance("X-n101-k25", "/path/to/instances/")
vrplib.download_solution("X-n101-k25", "/path/to/solutions/")

# List all instance names that can be downloaded 
vrplib.list_names()                      # All instance names
vrplib.list_names(low=100, high=200)     # Instances with between [100, 200] customers
vrplib.list_names(vrp_type="cvrp")       # Only CVRP instances
vrplib.list_names(vrp_type="vrptw")      # Only VRPTW instances
```


## Documentation
This section contains some documentation about the `vrplib` package.

### Instance formats
`vrplib` supports two VRP instance formats: VRPLIB and Solomon. 

#### VRPLIB format
The VRPLIB format is the standard format specification for Capacitated Vehicle Routing Problem (CVRP) instances, see the [X-n101-k25](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/X/X-n101-k25.vrp) instance for an example. 

An example of an VRPLIB instance looks as follows:
``` bash
KEY1: VALUE1
KEY2: VALUE2
DATA1_SECTION
1 1
2 3
DATA2_SECTION
1 0 0 0 0
2 0 0 0 0
EOF
```

A VRPLIB consists of a **specification** part and a **data** part. 
The specification part contains information on the file format and on its content. 
Each specification must be presented as a key-value pair, separated by a colon. 
The data part contains explicit problem data such as customer coordinates or service times.
Data sections must start with a section header (e.g., `SERVICE_TIME_SECTION`) followed by rows of data. 
Each row must start with the location index, starting from 1, followed by any number of white-space separated data.
There are two exceptions to this data section format: the `EDGE_WEIGHT_SECTION` and `DEPOT_SECTION`. These sections should not start with a location index for each row.

``` python
vrplib.read_vrplib("vrplib-instance.txt")

>>> TODO
```

The basic requirements are as follows:
- EDGE_WEIGHT_FORMAT: ...
- EDGE_WEIGHT_TYPE: ...

##### On computing distances 
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

Note that there are VRPLIB instances that use different rounding conventions in the literature, which may not be specified in the instance. For example, the X instance set proposed by [Uchoa et al. (2017)](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/new-instances) assumes that the distances are rounded to the nearest integer. 
When you use the `vrplib` package to read instances from the X set, it will return non-rounded Euclidean distances because the instance specifies the `EUC_2D` edge weight type which implies no rounding. 
This can be easily solved by rounding the distances matrix manually.

The VRPLIB format is an extension of the [TSPLIB95](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf) format. 
Additional information about the VRPLIB format can be found [here]( http://webhotel4.ruc.dk/~keld/research/LKH-3/LKH-3_REPORT.pdf).

#### Solomon format
The Solomon format was used to introduce the Solomon instances for the Vehicle Routing Problem with Time Window (VRPTW) and also the extended instance set by Homberger and Gehring. See the [C101](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/Solomon/C101.txt) instance for an example. 
`vrplib` supports this type of instance format because the aforementioned instances are widely used.

For Solomon-type instances, the default is to the Euclidean distances without rounding. 
A recent convention that was proposed during the [2021 DIMACS Vehicle Routing Implementation Challenge](http://dimacs.rutgers.edu/programs/challenge/vrp/vrptw/) is to truncate the Euclidean distances to one decimal. 
Similar to the X instance set, you can manually round the distances matrix to follow this convention.

### Other remarks
- The `XML100` benchmark set is not listed in `list_names` and cannot be downloaded through this package. You can download these instances directly from [CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/).

    
