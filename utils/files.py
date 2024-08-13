import os
import re
from zipfile import ZipFile


def make_dir(dir_name):
    base_dir = "/home/servers/"
    save_dir = os.path.join(base_dir, dir_name)
    os.makedirs(save_dir, exist_ok=True)
    return save_dir


def check_zip_file(filepath, pattern):
    return all(re.match(pattern, name) for name in ZipFile(filepath).namelist())


def unzip(filepath, location=None):
    return ZipFile(filepath).extractall(location)