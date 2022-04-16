from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import inspect
from itertools import combinations
from math import dist
import re
from typing import Optional


# TODO This is a shift variable to change all indices by IDX
# the convention in CVRPLIB is often to start with 1 index for DEPOT
DEPOT = 0
IDX = DEPOT - 1


class Parser:
    @staticmethod
    def from_file(
        instance_path: str, solution_path: Optional[str] = None,
    ):
        """
        Load the instance (and optionally the solution) from the
        provided paths.

        The default index for depot is 0 (CVRPLIB has 1 as convention).
        """
        instance = parse_instance(instance_path)

        if solution_path is not None:
            solution = parse_solution(solution_path)
            return instance, solution

        return instance


"""
Instance
"""


def parse_instance(path: str) -> Instance:
    with open(path, "r") as fi:
        # Everything in lowercase makes parsing easier
        lines = list(fi.read().lower().splitlines())

    metadata = parse_metadata(lines)
    sections = parse_sections(lines)
    all_data = create_additional(metadata | sections)

    return from_dict_to_dataclass(Instance, all_data)


def parse_metadata(lines: list[str]) -> dict[str, str]:
    """
    Parse the metadata at the beginning of the instance file.
    This data is formatted as KEY : VALUE lines.
    """
    data = {}
    for line in lines:
        if " : " in line:
            k, v = [x.strip() for x in line.split(" : ", 1)]
            data[k] = int(v) if v.isnumeric() else v
    return data


def parse_sections(lines):
    """
    Parse the sections data of the instance file. Sections start with a row
    containing NAME_SECTION followed by a number of lines with data.
    """
    name = None  # Used as key to store data
    sections = defaultdict(list)

    for line in lines:
        if "_section" in line:
            name = line.split("_section")[0].strip()

        elif "eof" in line:
            continue

        elif name:
            row = [float(num) for num in line.strip().split()]
            sections[name].append(row)

    data = {}

    for name, section in sections.items():
        if name == "demand":
            data["demands"] = [int(row[1]) for row in section]

        elif name == "depot":
            data["depot"] = int(section[0][0]) + IDX
            # TODO What is dummy?
            data["dummy"] = int(section[1][0]) + IDX

        elif name == "node_coord":
            data["coordinates"] = [[row[1], row[2]] for row in section]

        elif name == "edge_weight":
            data["edge_weight"] = [[int(num) for num in row] for row in section]

    return data


def create_additional(data: dict[str, ...]) -> dict[str, ...]:
    """
    Create all additional data for the creation of a full CVRP instance.

    Distances
    ---------
    Using the metadata "edge_weight_type" we can infer how to construct the
    distances: 1) either by computing the pairwise Euclidan distances
    using the provided coordinates or by 2) using the triangular matrix.
    """
    if "customers" not in data:
        n = data["dimension"]
        data["customers"] = [i for i in range(2 + IDX, n + 1)]

    if "distances" not in data:
        if data["edge_weight_type"] == "euc_2d":
            data["distances"] = euclidean(data["coordinates"])

        elif data["edge_weight_type"] == "explicit":
            if data["edge_weight_format"] == "lower_row":
                data["distances"] = from_triangular(data["edge_weight"])

    return data


def euclidean(coords: list[list[int, int]]) -> list[list[int]]:
    """
    Compute the pairwise Euclidean distances using the passed-in coordinates.
    """
    n = len(coords)
    distances = [list(0 for _ in range(n)) for _ in range(n)]

    for (i, coord_i), (j, coord_j) in combinations(enumerate(coords), r=2):
        d_ij = round(dist(coord_i, coord_j))  # Convention to round
        distances[i][j] = d_ij
        distances[j][i] = d_ij

    return distances


def from_triangular(triangular: list[list[int]]) -> list[list[int]]:
    """
    Compute a full distances matrix from a triangular matrix.
    """
    n = len(triangular) + 1
    distances = [list(0 for _ in range(n)) for _ in range(n)]

    for j, i in combinations(range(n), r=2):
        t_ij = triangular[i - 1][j]
        distances[i][j] = t_ij
        distances[j][i] = t_ij

    return distances


def from_dict_to_dataclass(cls, data):
    return cls(
        **{
            key: (data[key] if val.default == val.empty else data.get(key, val.default))
            for key, val in inspect.signature(Instance).parameters.items()
        }
    )


@dataclass
class Instance:
    name: str
    comment: str
    dimension: int
    capacity: int
    distances: list[float]
    coordinates: list[list[float]]
    demands: list[int]
    depot: int
    customers: list[int]


"""
Solution
"""


def parse_solution(path: str):
    """Extract the solution."""
    routes = []
    with open(path, "r") as fi:
        # Everything in lowercase makes parsing easier
        lines = list(fi.read().lower().splitlines())

        for line in lines:
            line = line.strip()
            if "route" in line:
                # TODO Split is not necessary; can match directly
                route = re.split(r"route #\d+: ", line)[1]
                route = [int(cust) + IDX for cust in route.split(" ") if cust]
                routes.append(route)

            elif "cost" in line:
                cost = line.lstrip("cost ")
                cost = int(cost) if cost.isdigit() else float(cost)

    return Solution(routes, cost)


@dataclass
class Solution:
    routes: list[int]
    cost: float | int


if __name__ == "__main__":
    # x = parse_instance("data/CVRPLIB/A/A-n32-k5.vrp")
    # x = parse_instance("data/CVRPLIB/D/ORTEC-n242-k12.vrp")

    inst_path = "data/CVRPLIB/D/ORTEC-n242-k12.vrp"
    sol_path = "data/CVRPLIB/D/ORTEC-n242-k12.sol"
    x = Parser.from_file(inst_path)
