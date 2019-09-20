from threading import Timer, start_new_thread
from functools import partial
from os import remove, path, stat, walk
from platform import system
from time import time


def get_file_name(fp: str) -> str:
    return path.splitext(fp)


def get_file_creation_date(fp: str) -> str:
    if system() == 'Windows':
        return path.getctime(fp)
    else:
        meta = stat(fp)
        try:
            return meta.st_birthtime
        except AttributeError:
            return meta.st_mtime


def get_all_files_in_dir(dir: str) -> list:
    fps = []

    for pack in walk(dir):
        for f in pack[2]:
            fps.append(f)

    return fps


def del_old_files_in_dir(path: str, age: int = 0):
    def _del_old_files_in_dir(path: str, age: int = 0):
        fps = get_all_files_in_dir()

        for fp in fps:
            crt_time = get_file_creation_date(fp)
            if time() - crt_time > age:
                start_new_thread(remove, fp)

    start_new_thread(_del_old_files_in_dir, path, age)


def del_old_files_in_dir_periodic(
        interval: int, path: str, age: int = 0):
    Timer(interval, partial(del_old_files_in_dir, age, path)).start()
