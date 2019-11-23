from threading import Timer, Thread
from functools import partial
from os import remove, path, stat, walk
from platform import system
from time import time
import zipfile as zf


def get_file_creation_date(filepath: str) -> str:
    if system() == "Windows":
        return path.getctime(filepath)
    else:
        meta = stat(filepath)
        try:
            return meta.st_birthtime
        except AttributeError:
            return meta.st_mtime


def get_all_files_in_dir(dir: str) -> list:
    filepaths = []

    for pack in walk(dir):
        for f in pack[2]:
            filepaths.append(f)

    return filepaths


def del_old_files_in_dir(path: str, age: int = 0):
    def _del_old_files_in_dir(path: str, age: int = 0):
        filepaths = get_all_files_in_dir()

        for filepath in filepaths:
            crt_time = get_file_creation_date(filepath)
            if time() - crt_time > age:
                Thread(target=remove, args=[filepath]).start()

    Thread(target=_del_old_files_in_dir, args=[path, age]).start()


def del_old_files_in_dir_periodic(interval: int, path: str, age: int = 0):
    Timer(interval, partial(del_old_files_in_dir, age, path)).start()
