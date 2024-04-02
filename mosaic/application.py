import os

import toml
from PySide6.QtWidgets import QApplication, QProxyStyle, QStyle, QStyleFactory
from qtawesome import icon

_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_project_toml = os.path.join(_project_root, "pyproject.toml")
_project_data = toml.load(_project_toml)


def _version() -> str:
    return _project_data["tool"]["poetry"]["version"]


class MosaicStyle(QProxyStyle):
    def __init__(self, base: QStyle):
        super().__init__(base)

    def standardIcon(self, standardIcon, option=None, widget=None):
        if standardIcon == QStyle.StandardPixmap.SP_TitleBarCloseButton:
            return icon("mdi6.window-close")
        elif standardIcon == QStyle.StandardPixmap.SP_TitleBarNormalButton:
            return icon("mdi6.dock-window")

        return super().standardIcon(standardIcon, option, widget)


class MosaicEditor(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setApplicationName("Mosaic Editor")
        self.setOrganizationName("Mosaic")
        self.setApplicationVersion(_version())
        self.setStyle(MosaicStyle(QStyleFactory.create("Fusion")))
