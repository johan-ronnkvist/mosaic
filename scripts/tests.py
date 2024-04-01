import os
import subprocess
import webbrowser


def project_folder(*args) -> str:
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(root, *args)


def codecov():
    command = "pytest --cov=mosaic . --cov-report=html"
    subprocess.run(command, check=True)
    webbrowser.open("file://" + os.path.realpath("htmlcov/index.html"))
