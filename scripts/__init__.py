import os


def openfile(filepath):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', filepath))
