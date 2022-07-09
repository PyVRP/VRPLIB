import re
from dataclasses import dataclass
from typing import Any, Dict, List

from .utils import from_dict_to_dataclass


@dataclass
class Solution:
    routes: List[int]
    cost: float


def parse_solution(lines: List[str]) -> Solution:
    """
    Extract the solution. Solutions contain routes, which are indexed
    from 1 to n.
    """

    def parse_routes(lines: List[str]) -> List[List[int]]:
        """
        Parse the lines to obtain the routes.
        """
        routes = []

        for line in lines:
            line = line.strip().lower()

            if "route" in line:
                # TODO Split is not necessary; can match directly
                route = re.split(r"route #\d+: ", line)[1]
                route = [int(cust) for cust in route.split(" ") if cust]
                routes.append(route)

        return routes

    def parse_cost(lines: List[str]) -> float:
        for line in lines:
            line = line.strip().lower()

            if "cost" in line:
                cost = line.lstrip("cost ")
                break

        return int(cost) if cost.isdigit() else float(cost)

    data: Dict[str, Any] = {}
    data["routes"] = parse_routes(lines)
    data["cost"] = parse_cost(lines)

    return from_dict_to_dataclass(Solution, data)
