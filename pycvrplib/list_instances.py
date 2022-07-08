import re
from functools import lru_cache
from typing import Dict, List, Optional

import requests

from .constants import MEDIA_URL


def list_instances() -> List[str]:
    """
    Return the names of all CVRPLIB instances that can be passed to the
    `download` function.
    """
    return get_names()


@lru_cache(1)
def get_names() -> List[str]:
    """
    A cached function that makes a call to the CVRPLIB media directory and
    returns a list of all instance names including set name.
    """
    response = requests.get(MEDIA_URL)

    if response.status_code != 200:
        response.raise_for_status()

    names = []
    for line in response.text.splitlines():

        if 'alt="[DIR]"' in line and "Parent Directory" not in line:
            set_name = between_a_tags(line)
            resp = requests.get(MEDIA_URL + set_name)

            for line in resp.text.splitlines():
                if ".vrp" in line:
                    data = between_a_tags(line)
                    if data.endswith(".vrp"):
                        names.append(set_name + data.rstrip(".vrp"))

                if ".txt" in line:
                    data = between_a_tags(line)
                    if data.endswith(".txt"):
                        names.append(set_name + data.rstrip(".txt"))
    return names


def between_a_tags(line: str) -> str:
    """
    HACK Get the content between <a href></a> tags.
    """
    return re.findall(r"<a href.*?>(.*?)</a>", line)[0]
