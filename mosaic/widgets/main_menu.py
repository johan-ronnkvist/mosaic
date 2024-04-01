from PySide6.QtWidgets import QMenuBar, QMenu


class MainMenu(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._file = self.addMenu("&File")
        self._edit = self.addMenu("&Edit")
        self._view = self.addMenu("&View")
        self._help = self.addMenu("&Help")

    @property
    def file(self) -> QMenu:
        return self._file

    @property
    def edit(self) -> QMenu:
        return self._edit

    @property
    def view(self) -> QMenu:
        return self._view

    @property
    def help(self) -> QMenu:
        return self._help
