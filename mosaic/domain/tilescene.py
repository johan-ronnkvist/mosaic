from typing import Protocol

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import QGraphicsScene, QGraphicsItem


class Coordinate(Protocol):
    pass


class Tile(Protocol):
    def coordinate(self) -> Coordinate: ...


class TileModel(Protocol):
    def insert(self, tile: Tile): ...

    def remove(self, tile: Tile | Coordinate): ...

    def tile_at(self, coordinate: Coordinate) -> Tile | None: ...


class TileScene(QGraphicsScene):
    def __init__(self):
        super().__init__()

        # self.create_tiles(10, 15, 50)
        self.create_boundary(QSize(30, 20), QSize(32, 32))

    def create_tiles(
        self,
        rows: int,
        cols: int,
        size: int,
    ):
        for row in range(rows):
            for col in range(cols):
                item = self.addRect(col * size, row * size, size, size)
                item.setFlag(QGraphicsItem.ItemIsSelectable)
                r = int(255 - row * 255 / (rows - 1))
                g = int(255 - col * 255 / (cols - 1))
                b = int(255 - (row + col) * 255 / (rows + cols))
                item.setBrush(QBrush(QColor(r, g, b)))

    def create_boundary(self, grid_size: QSize, cell_size: QSize):
        item = self.addRect(0, 0, grid_size.width() * cell_size.width(), grid_size.height() * cell_size.height())
        item.setFlag(QGraphicsItem.ItemIsSelectable)
        # red pen, 2px width
        item.setPen(QPen(Qt.red, 2))

        # item.setZValue(-1)
