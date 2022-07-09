from pycvrplib import read


def test_C101():
    instance = read("data/C101.txt")
    N = 100

    assert instance.name == "C101"
    assert instance.dimension == N + 1
    assert instance.n_customers == N
    assert instance.depot == 0
    assert instance.customers == list(range(1, N + 1))
    assert instance.n_vehicles == 25
    assert instance.capacity == 200
    assert instance.coordinates[N] == [55, 85]
    assert instance.distances[0][1] == 19
    assert instance.demands[N] == 20
    assert instance.service_times[N] == 90
    assert instance.earliest[N] == 647
    assert instance.latest[N] == 726
