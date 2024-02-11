from PySide6.QtWidgets import QMenuBar, QMenu


class MainMenu(QMenuBar):
    def __init__(self, parent=None):
        super(MainMenu, self).__init__(parent)
        self.parent = parent
        self._file = self.addMenu("&File")

    @property
    def file(self) -> QMenu:
        return self.addMenu("&File")
