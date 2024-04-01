from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QGraphicsView

from mosaic.domain.tilescene import TileScene
from mosaic.utils.scene_select_tool import SelectionTool
from mosaic.utils.scene_zoom_tool import SceneZoomTool, GraphicsViewPan


class SceneView(QGraphicsView):
    def __init__(self, scene: TileScene, parent=None):
        super().__init__(parent)
        self.setScene(scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setRenderHint(QPainter.TextAntialiasing)

        self._zoom = SceneZoomTool(self)
        self._pan = GraphicsViewPan(self)
        self._select = SelectionTool(self)
