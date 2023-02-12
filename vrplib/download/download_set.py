import urllib
import zipfile


def download_set(set_name, out_dir):
    url = "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/Vrp-Set-Solomon.zip"

    zip_path, _ = urllib.request.urlretrieve(url)
    with zipfile.ZipFile(zip_path, "r") as f:
        f.extractall(out_dir)
