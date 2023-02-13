import urllib
import zipfile

from .constants import CVRP_SETS, VRPTW_SETS


def download_set(set_name, out_dir):
    if set_name not in CVRP_SETS + VRPTW_SETS:
        raise ValueError(f"Instance set {set_name} is not known.")

    # TODO find set name
    url = "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/Vrp-Set-Solomon.zip"
    zip_path, _ = urllib.request.urlretrieve(url)

    with zipfile.ZipFile(zip_path, "r") as f:
        f.extractall(out_dir)
