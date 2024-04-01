import logging

from PySide6.QtCore import QObject, Qt, QEvent
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QGraphicsView

_logger = logging.getLogger(__name__)


class SelectionTool(QObject):
    def __init__(self, view: QGraphicsView):
        super().__init__(view)  # Pass the view as the parent to ensure proper cleanup
        self._view = view
        self._scene = view.scene()
        self._view.viewport().installEventFilter(self)

    def eventFilter(self, _watched, event) -> bool:
        if isinstance(event, QMouseEvent):
            position = self._view.mapToScene(event.pos())
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                if Qt.ControlModifier not in event.modifiers():
                    self._scene.clearSelection()
                if item := self._scene.itemAt(position, self._view.transform()):
                    item.setSelected(True)
                    return True
            elif event.type() == QEvent.MouseMove and event.buttons() & Qt.LeftButton:
                if item := self._scene.itemAt(position, self._view.transform()):
                    item.setSelected(True)
                    return True
        return False
