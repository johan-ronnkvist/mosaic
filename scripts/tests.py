import os
import subprocess


def project_folder(*args) -> str:
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(root, *args)


def codecov():
    command = "pytest --cov=mosaic ."
    subprocess.run(command, check=True)
