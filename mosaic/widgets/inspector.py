from typing import Protocol

from PySide6.QtWidgets import QWidget, QDockWidget, QVBoxLayout


class InspectableEntity(Protocol):
    def inspect(self, parent: QWidget) -> QWidget: ...


class InspectWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setLayout(QVBoxLayout())


class Inspector(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setMinimumWidth(200)


class InspectDockable(QDockWidget):
    def __init__(self, inspector: Inspector, parent: QWidget = None):
        super().__init__(parent)
        self.setWindowTitle("Inspector")
        self.setWidget(inspector)
