from typing import Dict, List, Union


def parse_solution(lines: List[str]) -> Dict[str, Union[List, float]]:
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

            if line.startswith("route"):
                route = [  # type:ignore
                    int(cust) for cust in line.split(":")[1].split(" ") if cust
                ]
                routes.append(route)

        return routes

    def parse_cost(lines: List[str]) -> float:
        for line in lines:
            line = line.strip().lower()

            if "cost" in line:
                cost = line.lstrip("cost ")
                break

        return int(cost) if cost.isdigit() else float(cost)

    data: Dict[str, Union[List, float]] = {}
    data["routes"] = parse_routes(lines)
    data["cost"] = parse_cost(lines)

    return data
