import os

def make_dir(dir_name):
    base_dir = "/home/servers/"
    save_dir = os.path.join(base_dir, dir_name)
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    return save_dir


def check_files(directory, pattern):
    print(os.listdir(directory))
