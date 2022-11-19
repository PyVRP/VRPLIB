import numpy as np


def write(path, instance, name="problem", euclidean=False, is_vrptw=True):
    with open(path, "w") as f:
        capacity = instance["capacity"]
        dimension = len(instance["coords"])
        comment = ...
        vrp_type = ...
        write_preamble(
            f, name, comment, vrp_type, dimension, euclidean, capacity
        )

        if not euclidean:
            write_edge_weights(f, instance["duration_matrix"])

        # Write data sections
        write_coords(f, instance["coords"])
        write_demands(f, instance["demands"])
        write_is_depot(f, instance["is_depot"])

        if is_vrptw:
            write_service_times(f, instance["service_times"])
            write_time_windows(f, instance["time_windows"])
            write_release_times(f, instance["release_times"])

        f.write("EOF\n")


def write_preamble(f, name, comment, vrp_type, dimension, euclidean, capacity):
    preamble = [
        ("NAME", name),
        ("COMMENT", comment),
        # For HGS we need an extra row... # TODO check this
        ("TYPE", vrp_type),
        ("DIMENSION", dimension),
        ("EDGE_WEIGHT_TYPE", "EUC_2D" if euclidean else "EXPLICIT"),
        ([] if euclidean else [("EDGE_WEIGHT_FORMAT", "FULL_MATRIX")]),
        [("CAPACITY", capacity)],
    ]

    f.write("\n".join([f"{k} : {v}" for k, v in preamble]))
    f.write("\n")


def write_edge_weights(f, duration_matrix):
    f.write("EDGE_WEIGHT_SECTION\n")

    for row in duration_matrix:
        f.write("\t".join(map(str, row)))
        f.write("\n")


def write_coords(f, coords):
    f.write("NODE_COORD_SECTION\n")
    f.write(
        "\n".join([f"{idx}\t{x}\t{y}" for idx, (x, y) in enumerate(coords, 1)])
    )
    f.write("\n")


def write_demands(f, demands):
    write_section(f, "DEMAND", demands)


def write_is_depot(f, is_depot):
    f.write("DEPOT_SECTION\n")

    for i in np.flatnonzero(is_depot):
        f.write(f"{i+1}\n")
        f.write("-1\n")


def write_service_times(f, service_times):
    write_section(f, "SERVICE_TIME", service_times)


def write_time_windows(f, tw):
    f.write("TIME_WINDOW_SECTION\n")
    f.write(
        "\n".join([f"{idx}\t{l}\t{u}" for idx, (l, u) in enumerate(tw, 1)])
    )
    f.write("\n")


def write_release_times(f, release_times):
    write_section(f, "RELEASE_TIME", release_times)


def write_section(f, name, data):
    # TODO make this work for data with more than 1 dimension
    f.write(f"{name}_SECTION\n")
    f.write("\n".join([f"{idx}\t{s}" for idx, s in enumerate(data, 1)]))
    f.write("\n")
