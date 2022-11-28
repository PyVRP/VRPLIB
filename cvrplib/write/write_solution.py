from typing import Dict, List, Union

SolutionData = Union[int, float, str, List[List[int]]]


def write_solution(path: str, solution: Dict[str, SolutionData]):
    """
    Writes a VRP solution to file following # TODO
    """

    with open(path, "w") as fi:
        for k, v in solution.items():
            if k == "routes":
                for idx, route in enumerate(v, 1):  # type: ignore
                    fi.write(
                        f"Route {idx} : {' '.join([str(s) for s in route])}"
                    )
                    fi.write("\n")
            else:
                fi.write(f"{k.capitalize()} : {v}")
                fi.write("\n")
