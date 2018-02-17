
import os


def resolve_path(path):
    return os.path.abspath(os.path.expanduser(path))
