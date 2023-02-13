from dataclasses import dataclass
from pathlib import Path

from vrplib.download.download_utils import find_set

CVRPLIB_DATA_DIR = Path("tests/data/cvrplib/")


@dataclass
class Case:
    name: str
    set_name: str
    instance_name: str
    instance_path: str
    solution_path: str
    dimension: int
    capacity: int
    cost: float


def make_case(
    set_name,
    instance_name,
    dimension,
    capacity,
    cost,
):
    """
    Return a test case based on the passed-in arguments.
    """
    return Case(
        name=set_name + "/" + instance_name,
        set_name=set_name,
        instance_name=instance_name,
        instance_path=CVRPLIB_DATA_DIR
        / (
            instance_name
            + (
                ".txt"
                if find_set(instance_name) in ["Solomon", "HG"]
                else ".vrp"
            )
        ),
        solution_path=CVRPLIB_DATA_DIR / (instance_name + ".sol"),
        dimension=dimension,
        capacity=capacity,
        cost=cost,
    )


def selected_cases():
    """
    A selection of test cases.
    """
    A = make_case("A", "A-n32-k5", 32, 100, 784)
    B = make_case("B", "B-n31-k5", 31, 100, 672)
    C = make_case("CMT", "CMT6", 51, 160, 555.43)
    D = make_case("D", "ORTEC-n242-k12", 242, 125, 123750)
    E = make_case("E", "E-n13-k4", 13, 6000, 247)
    F = make_case("F", "F-n72-k4", 72, 30000, 237)
    G = make_case("Golden", "Golden_1", 241, 550, 5623.47)
    L = make_case("Li", "Li_21", 561, 1200, 16212.82548)
    M = make_case("M", "M-n101-k10", 101, 200, 820)
    P = make_case("P", "P-n16-k8", 16, 35, 450)
    X = make_case("X", "X-n101-k25", 101, 206, 27591)

    return [
        A,
        B,
        C,
        D,
        E,
        F,
        G,
        L,
        M,
        P,
        X,
    ]
