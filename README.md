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

### VRPLIB instance format
The VRPLIB format is the standard format for the Capacitated Vehicle Routing Problem (CVRP). An example of an VRPLIB instance looks as follows:
``` bash
NAME: Example 
EDGE_WEIGHT_TYPE: EUC_2D
NODE_COORD_SECTION
1 0 0
2 5 5
SERVICE_TIME_SECTION
1 0
2 3
DEPOT_SECTION
1
EOF
```

A VRPLIB consists of a **specification** part and a **data** part. 
- The specification part contains information about the file format and on its content. Each specification should be presented as a key-value pair separated by a colon. In the example above, `NAME` and `EDGE_WEIGHT_TYPE` are the specifications.
- The data part contains explicit problem data such as customer coordinates or service times. 
Each data section starts with a header name that ends with `_SECTION`, e.g., `SERVICE_TIME_SECTION` and `NODE_COORD_SECTION`.
The section is then followed by rows of array-like data, and each row must start with the location index, starting from 1, followed by any number of white-space separated data.
There are two exceptions to this rule: the `EDGE_WEIGHT_SECTION` and `DEPOT_SECTION` should not start with a location index for each row.

Except for the rules outlined above, `vrplib` is not strict about the naming of specifications or sections. 
This means that you can use `vrplib` to read VRPLIB instances with custom specifications and section names like `MY_SECTION`.

Reading the above example instance returns the following:
``` python
vrplib.read_vrplib("vrplib-example.txt")

>>> {'name': 'Example',
     'edge_weight_type': 'EUC_2D',
     'node_coord': array([[0, 0], [5, 5]]),
     'service_time': array([1, 3]),
     'edge_weight': array([[0.  , 7.07106781], [7.07106781, 0.  ]]),
     'depot': array([0])}
```


#### On computing distances 
The `vrplib` library tries to follow the instance specifications as strictly as possible to compute the distances. 

For VRPLIB instances, the distances computation is determined by the `EDGE_WEIGHT_TYPE` and possibly the `EDGE_WEIGHT_FORMAT` specifications. We currently support two categories of edge weight types:
- `*_2D`: compute the Euclidean distances using the node coordinate data.
    - `EUC_2D`: Double precision distances without rounding.
    - `FLOOR_2D`: Round down all distances to down to an integer.
    - `EXACT_2D`: Multiply the distances by 1000, round to the nearest integer.
- `EXPLICIT`: the distance data is explicitly provided, in partial or full form. For explicit matrices, the `EDGE_WEIGHT_FORMAT` must be specified. We support the following two formats:
  - `LOWER_ROW`: Lower row triangular matrix without diagonal entries.  
  - `FULL_MATRIX`: Explicit full matrix representation.
  

The VRPLIB format is an extension of the [TSPLIB95](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf) format. 
Additional information about the VRPLIB format can be found [here]( http://webhotel4.ruc.dk/~keld/research/LKH-3/LKH-3_REPORT.pdf).

### Solomon format
The Solomon format was used to introduce the Solomon instances for the Vehicle Routing Problem with Time Window (VRPTW) and also the extended instance set by Homberger and Gehring. See the [C101](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/Solomon/C101.txt) instance for an example. 
`vrplib` supports this type of instance format because the aforementioned instances are widely used.
For Solomon-type instances, the default is to the Euclidean distances without rounding.
TODO 

## Other remarks
- The `XML100` benchmark set is not listed in `list_names` and cannot be downloaded through this package. You can download these instances directly from [CVRPLIB](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/).
- In the literature, some instances use rounding conventions different from what is specified in the instance. For example, X instance set proposed by [Uchoa et al. (2017)](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/new-instances) assumes that the distances are rounded to the nearest integer. When you use the `vrplib` package to read this instance, it will return non-rounded Euclidean distances because the instance specifies the `EUC_2D` edge weight type which implies no rounding. To adhere to the convention used in the literature, you can manually round the distances matrix.
