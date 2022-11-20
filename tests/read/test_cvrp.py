from cvrplib import read


def test_X_n101_k25():
    instance = read("data/X-n101-k25.vrp")

    assert instance["name"] == "X-n101-k25"
    assert instance["dimension"] == 101
    assert instance["n_customers"] == 100
    assert instance["depot"] == 0
    assert instance["customers"] == list(range(1, 101))
    assert instance["capacity"] == 206
    assert instance["distance_limit"] == float("inf")
    assert instance["demands"][100] == 35
    assert instance["coordinates"][100] == [615, 750]
    assert instance["service_times"][0:2] == [0, 0]


def test_CMT6():
    """
    CMT6 instance contains the fields ``distance_limit`` and ``service_time``.
    """
    instance = read("data/CMT6.vrp")
    N = 50

    assert instance["name"] == "CMT6"
    assert instance["dimension"] == N + 1
    assert instance["n_customers"] == N
    assert instance["depot"] == 0
    assert instance["customers"] == list(range(1, N + 1))
    assert instance["capacity"] == 160
    assert instance["distance_limit"] == 200
    assert instance["demands"][N] == 10
    assert instance["coordinates"][N] == [56, 37]
    assert instance["service_times"][0:2] == [0, 10]
