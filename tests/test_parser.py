import pytest
import glob

from ..Parser import Parser


def all_complete_paths():
    SET = "D"

    instance_names = set(
        fname.rstrip(".vrp")
        for fname in glob.iglob(f"./**/{SET}/*.vrp", recursive=True)
    )
    solution_names = set(
        fname.rstrip(".sol")
        for fname in glob.iglob(f"./**/{SET}/*.sol", recursive=True)
    )
    complete_names = set(
        (f"{name}.vrp", f"{name}.sol") for name in instance_names & solution_names
    )

    return complete_names


@pytest.mark.parametrize("instance_path, solution_path", all_complete_paths())
def test_distances(instance_path, solution_path):

    pass
