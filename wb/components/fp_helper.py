from os.path import isfile
from re import match


def is_filepath_valid(filepath: str) -> bool:
    return match('^((\w:/)|//|/|./|\.\./)?(\w+/)*(\w+\.\w+)$', filepath) and filepath


def is_filepath_valid_and_exists(filepath: str) -> bool:
    return is_filepath_valid(filepath=filepath) and isfile(filepath)
