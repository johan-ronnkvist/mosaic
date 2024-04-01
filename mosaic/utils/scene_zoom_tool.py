from PySide6.QtCore import QObject, Qt, QPointF
from PySide6.QtGui import QWheelEvent, QKeyEvent
from PySide6.QtWidgets import QGraphicsView


class SceneZoomTool(QObject):
    def __init__(self, view: QGraphicsView):
        super().__init__()
        self._view = view
        self._zoom_factor = 1.0015
        self._zoom_modifier = Qt.ControlModifier
        self._install_event_filter(view)

    def _install_event_filter(self, view: QGraphicsView):
        view.viewport().installEventFilter(self)
        view.setMouseTracking(True)

    def zoom(self, delta: float, pos: QPointF):
        factor = self._zoom_factor**delta
        self._view.scale(factor, factor)
        self._view.centerOn(pos)

    def eventFilter(self, _watched, event) -> bool:
        if isinstance(event, QWheelEvent):
            if self._zoom_modifier in event.modifiers():
                scroll = event.angleDelta().y()
                self.zoom(scroll, event.position())
                return True

        return False


class GraphicsViewPan(QObject):
    def __init__(self, view: QGraphicsView):
        super().__init__()
        self._view = view
        self._pan_modifier = Qt.ControlModifier

        self._install_event_filter(view)

    def _install_event_filter(self, view: QGraphicsView):
        view.installEventFilter(self)
        view.setMouseTracking(True)

    def eventFilter(self, _watched, event) -> bool:
        if event.type() == QKeyEvent.Type.KeyPress:
            if event.key() == Qt.Key_Space:
                if self._view.dragMode() != QGraphicsView.DragMode.ScrollHandDrag:
                    self._view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        if event.type() == QKeyEvent.Type.KeyRelease:
            if event.key() == Qt.Key_Space:
                if self._view.dragMode() == QGraphicsView.DragMode.ScrollHandDrag:
                    self._view.setDragMode(QGraphicsView.DragMode.NoDrag)

        return False
