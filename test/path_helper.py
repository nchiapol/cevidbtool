import sys, os

def add_path(path = ".."):
    path = os.path.abspath(path)
    if path not in sys.path:
       sys.path.insert(0, path)

