import re
from typing import Dict, List, Tuple, Union

import numpy as np

from .parse_distances import parse_distances
from .parse_utils import infer_type, text2lines

Instance = Dict[str, Union[str, float, np.ndarray]]


def parse_vrplib(text: str, compute_edge_weights: bool = True) -> Instance:
    """
    Parses a VRPLIB instance. An instance consists of two parts:
    1) Specifications: single line of the form <KEY>:<VALUE>.
    2) Data sections: starts with <KEY>_SECTION, followed by rows of values.

    Each specification is parsed as keyword-value pair, where the keyword is
    given lowercase and the value is unmodified. From each data section the
    name is parsed in lower case without the "_SECTION". The data values are
    parsed as numpy arrays, where customer indices are removed (if applicable).

    Parameters
    ----------
    text
        The instance text.
    compute_edge_weights
        Whether to compute edge weights from the node coordinates.
        Defaults to True.

    Returns
    -------
    dict
        The instance data.
    """
    instance = {}

    specs, sections = group_specifications_and_sections(text2lines(text))

    for spec in specs:
        key, value = parse_specification(spec)
        instance[key] = value

    for section in sections:
        section, data = parse_section(section, instance)
        instance[section] = data

    if instance and compute_edge_weights and "edge_weight" not in instance:
        # Compute edge weights if there was no explicit edge weight section
        edge_weights = parse_distances([], **instance)  # type: ignore
        instance["edge_weight"] = edge_weights

    return instance


def group_specifications_and_sections(lines: List[str]):
    """
    Groups instance lines into specifications and section parts.
    """
    specs = []
    sections = []

    end_section = 0
    for idx, line in enumerate(lines):
        if "EOF" in line:
            break
        elif idx < end_section:  # Skip all lines of the current section
            continue
        elif ":" in line:
            specs.append(line)
        elif "_SECTION" in line:
            start = lines.index(line)
            end_section = start + 1

            for next_line in lines[start + 1 :]:
                # The current section ends when a next section or an EOF token
                # is found.
                if "_SECTION" in next_line or "EOF" in next_line:
                    break

                end_section += 1

            sections.append(lines[start:end_section])
        else:
            msg = "Instance does not conform to the VRPLIB format."
            raise RuntimeError(msg)

    return specs, sections


def parse_specification(line: str) -> Tuple[str, Union[float, str]]:
    """
    Parses a specification line as keyword-value pair, split at the first colon
    occurrence. The keyword is made lowercase and the value is unmodified.
    """
    k, v = [x.strip() for x in re.split("\\s*:\\s*", line, maxsplit=1)]
    return k.lower(), infer_type(v)


def parse_section(lines: List, instance: Dict) -> np.ndarray:
    """
    Parses the data section into numpy arrays.
    """
    section = _remove_suffix(lines[0].strip(), "_SECTION").lower()
    data_ = [[infer_type(n) for n in line.split()] for line in lines[1:]]

    if section == "edge_weight":
        # Parse separately because it may require additional processing
        return section, parse_distances(data_, **instance)  # type: ignore

    data = np.array(data_)

    if section == "depot":
        # Remove -1 end token and renormalize depots to start at zero
        data = data[data != -1] - 1
    else:
        # We remove the customer indices column from non-depot section
        data = data[:, 1:]

    # Squeeze data sections that contain only one column
    if data.ndim > 1 and data.shape[-1] == 1:
        data = data.squeeze(-1)

    return section, data


def _remove_suffix(name: str, suffix: str):
    return name[: -len(suffix)] if name.endswith(suffix) else name
