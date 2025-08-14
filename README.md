# VRPLIB
[![PyPI version](https://badge.fury.io/py/vrplib.svg)](https://badge.fury.io/py/vrplib)
[![vrplib](https://github.com/leonlan/vrplib/actions/workflows/vrplib.yml/badge.svg)](https://github.com/leonlan/vrplib/actions/workflows/vrplib.yaml)
[![codecov](https://codecov.io/gh/leonlan/VRPLIB/branch/master/graph/badge.svg?token=X0X66LBNZ7)](https://codecov.io/gh/leonlan/VRPLIB)

`vrplib` is a Python package for working with Vehicle Routing Problem (VRP) instances. The main features are:
- reading VRPLIB and Solomon instances and solutions, and
- writing VRPLIB-style instances and solutions.

## Outline
- [Installation](#installation)
- [Example usage](#example-usage)
- [Documentation](#documentation)

## Installation
`vrplib` only depends on `numpy` and may be installed in the usual way as

```shell
pip install vrplib
```

## Example usage
### Reading files
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
>>> instance.keys()
dict_keys(['name', ..., 'edge_weight'])

>>> solution.keys()
dict_keys(['routes', 'cost'])
```


### Writing files
The functions `write_instance` and `write_solution` provide a simple interface to writing instances and solutions in VRPLIB-style:
- `write_instance` adds indices to data sections when necessary (`EDGE_WEIGHT_SECTION` and `DEPOT_SECTION` are excluded).
- `write_solution` adds the `Route #{idx}` prefix to routes.

Note that these functions do not validate instances: it is up to the user to write correct VRPLIB-style files.

#### Instances
``` python
import vrplib

instance_loc = "instance.vrp"
instance_data = {
    "NAME": "instance",
    "TYPE": "CVRP",
    "VEHICLES": 2,
    "DIMENSION": 1,
    "CAPACITY": 1,
    "EDGE_WEIGHT_TYPE": "EUC_2D",
    "NODE_COORD_SECTION": [[250, 250], [500, 500]],
    "DEMAND_SECTION": [1, 1],
    "DEPOT_SECTION": [1],
}

vrplib.write_instance(instance_loc, instance_data)
```

``` 
NAME: instance
TYPE: CVRP
VEHICLES: 2
DIMENSION: 1
CAPACITY: 1
EDGE_WEIGHT_TYPE: EUC_2D
NODE_COORD_SECTION
1	250	250
2	500	500
DEMAND_SECTION
1	1
2	1
DEPOT_SECTION
1
EOF
```

#### Solutions
``` python
import vrplib

solution_loc = "solution.sol"
routes = [[1], [2, 3], [4, 5, 6]]
solution_data = {"Cost": 42, "Vehicle types": [1, 2, 3]}

vrplib.write_solution(solution_loc, routes, solution_data)
```

``` { .html } 
Route #1: 1
Route #2: 2 3
Route #3: 4 5 6
Cost: 42
Vehicle types: [1, 2, 3]
```



## Documentation
- [VRPLIB instance format](#vrplib-instance-format)
- [Solomon instance format](#solomon-instance-format)
- [Solution format](#solution-format)
- [Other remarks](#other-remarks)

### VRPLIB instance format
The VRPLIB format is the standard format for the Capacitated Vehicle Routing Problem (CVRP). An example VRPLIB instance looks as follows:
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

A VRPLIB instance contains problem **specifications** and problem **data**. 
- Specifications are key-value pairs separated by a colon. In the example above, `NAME` and `EDGE_WEIGHT_TYPE` are the two data specifications.
- Data are explicit array-like values such as customer coordinates or service times. 
Each data section should start with a header name that ends with `_SECTION`, e.g., `NODE_COORD_SECTION` and `SERVICE_TIME_SECTION`. It is then followed by rows of values and each row must start with an index representing the depot or customer. 
There are two exceptions: values in `EDGE_WEIGHT_SECTION` and `DEPOT_SECTION` should not start with an index.

Besides the rules outlined above, `vrplib` is not strict about the naming of specifications or sections. 
This means that you can use `vrplib` to read VRPLIB instances with custom specifications like `MY_SPECIFICATION: SOME_VALUE` and custom section names like `MY_SECTION`.

Reading the above example instance returns the following dictionary:
``` python
{'name': 'Example',
 'edge_weight_type': 'EUC_2D',
 'node_coord': array([[0, 0], [5, 5]]),
 'service_time': array([1, 3]),
 'depot': array([0]),
 'edge_weight': array([[0.  , 7.07106781], [7.07106781, 0.  ]])}
```

The depot section specifies which location index corresponds to the depot data. 
The convention is to let index 1 represent the depot. 
`vrplib` subtracts one from the depot value to make it easier to index.

#### Computing edge weights 
Note that the example instance did not include any explicit information about the edge weights, yet the output includes edge weights data.
This is because `vrplib` automatically computes the edge weights based on the instance specifications, if applicable.
In the example, the edge weight type specification and node coordinates data are used to compute the Euclidean distance.
You can set the `compute_distances` argument in `read_instance` to disable this feature.

Following the VRPLIB conventions, the edge weights are computed based on the `EDGE_WEIGHT_TYPE` specification, and in some cases the `EDGE_WEIGHT_FORMAT` specification. `vrplib` currently supports two categories of edge weight types:
- `*_2D`: Euclidean distances based on the node coordinates data.
    - `EUC_2D`: Double precision distances without rounding.
    - `FLOOR_2D`: Round down all distances to an integer.
    - `CEIL_2D`: Round up all distances to an integer.
    - `EXACT_2D`: Multiply the distances by 1000, round to the nearest integer.
- `EXPLICIT`: the distance data is explicitly provided, in partial or full form. The `EDGE_WEIGHT_FORMAT` specification must be present. We support the following two edge weight formats:
  - `LOWER_ROW`: Lower row triangular matrix without diagonal entries.
  - `FULL_MATRIX`: Explicit full matrix representation.
  

#### Line comments
Lines starting with `#` are interpreted as comments and not parsed when reading the instance.

#### More information about VRPLIB
The VRPLIB format is an extension of the [TSPLIB95](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf) format. 
Additional information about the VRPLIB format can be found [here]( http://webhotel4.ruc.dk/~keld/research/LKH-3/LKH-3_REPORT.pdf).

### Solomon instance format
The Solomon format was used to introduce the Solomon instances for the Vehicle Routing Problem with Time Window (VRPTW) and also the extended instance set by Homberger and Gehring. A Solomon instance looks like this:
``` bash
Example

VEHICLE
NUMBER     CAPACITY
  50          200

CUSTOMER
CUST NO.  XCOORD.    YCOORD.    DEMAND   READY TIME  DUE DATE   SERVICE TIME
    0      70         70          0          0       1351          0
    1      33         78         20        750        809         90
```

Reading this Solomon instance returns the following dictionary:
``` python
{'name': 'Example',
 'vehicles': 50,
 'capacity': 200,
 'node_coord': array([[70, 70], [33, 78]]),
 'demand': array([ 0, 20]),
 'time_window': array([[ 0, 1351], [ 750,  809]]),
 'service_time': array([ 0, 90]),
 'edge_weight': array([[ 0.  , 37.85498646], [37.85498646,  0.  ]])}
```

The edge weights are computed by default using the Euclidean distances. 

### Solution format
Here's an example of a solution format:
``` { .html } 
Route #1: 1 2 3
Route #2: 4 5
Cost: 100
```

A solution is represented by a set of routes, where each route specifies the sequence of customers to visit. 
Each route should start with "Route", followed by the route number, and followed by a colon. 
The customers to be served on the route are then listed.
The solution file can also include other keywords like `Cost`, which will be separated on the first colon or whitespace.

The convention is that customer indices start counting from 1, but `vrplib` simply parses the file without strict requirements about those indices.

Reading the above example solution returns the following dictionary:
``` python
{'routes': [[1, 2, 3], [4, 5]], 'cost': 100}
```

### Other remarks
- In the literature, some instances use rounding conventions different from what is specified in the instance. For example, X instance set proposed by [Uchoa et al. (2017)](http://vrp.atd-lab.inf.puc-rio.br/index.php/en/new-instances) assumes that the distances are rounded to the nearest integer. When you use the `vrplib` package to read this instance, it will return non-rounded Euclidean distances because the instance specifies the `EUC_2D` edge weight type which implies no rounding. To adhere to the convention used in the literature, you can manually round the distances matrix.
- For large instances (>5000 customers) it's recommended to set the `compute_edge_weights` argument to `False` in `read_instance`.
