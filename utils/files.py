import os
import re
from zipfile import ZipFile


def make_dir(dir_name):
    base_dir = "/home/servers/"
    save_dir = os.path.join(base_dir, dir_name)
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    return save_dir


def check_zip_file(file_location, pattern):
    return all(re.match(pattern, name) for name in ZipFile(file_location).namelist())
