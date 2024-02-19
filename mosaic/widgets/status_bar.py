from PySide6.QtWidgets import QStatusBar

from mosaic.widgets import factory


class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)


factory.register(StatusBar)
