import os
from pathlib import Path


#ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
ROOT_DIR =  str(Path(__file__).parent.parent)

def static_path(filename: str = ""):
    return os.path.join(ROOT_DIR, "static", filename)

def template_path():
    pass

def save_static_file(filename, content):
    with open(static_path(filename), "wb") as f:
        f.write(content)