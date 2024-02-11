import os

import toml
from PySide6.QtWidgets import QApplication

_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_project_toml = os.path.join(_project_root, "pyproject.toml")
_project_data = toml.load(_project_toml)


def _version() -> str:
    return _project_data["tool"]["poetry"]["version"]


class MosaicEditor(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setApplicationName("Mosaic Editor")
        self.setOrganizationName("Mosaic")
        self.setApplicationVersion(_version())
