from typing import Dict, List, Union

Solution = Dict[str, Union[int, float, str, List[List[int]]]]


def write_solution(path: str, solution: Solution):
    """
    Writes a VRP solution to file following the VRPLIB convention.

    path
        The file path.
    solution
        The dictionary containing solution data.

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
