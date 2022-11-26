import warnings
from functools import lru_cache

from .download_instance import download_instance
from .download_solution import download_solution


@lru_cache()
def download(name: str, solution: bool = False):
    """
    Downloads the instance from CVRPLIB directly. If `solution` is set, then
    also download the corresponding solution.
    """
    message = (
        "cvrplib.download has been deprecated in favor of "
        "cvrplib.download_instance and cvrplib.download_solution."
    )
    warnings.warn(message, DeprecationWarning, stacklevel=2)

    instance = download_instance(name)

    if not solution:
        return instance

    return instance, download_solution(name)
