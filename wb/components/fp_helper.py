from os.path import isfile
from re import match


def is_filepath_valid(self, filepath: str) -> bool:
    return match('^((\w:/)|//|/|./|\.\./)?(\w+/)*(\w+\.\w+)$', filepath) and filepath


def is_filepath_valid_and_exists(self, filepath: str) -> bool:
    return self._is_filepath_valid(filepath=filepath) and isfile(filepath)
