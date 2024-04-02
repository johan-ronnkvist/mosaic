import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow
from qtawesome import icon

from mosaic import actions
from mosaic.widgets.graphics_view import GraphicsView
from mosaic.widgets.inspector import InspectDockable
from mosaic.widgets.main_menu import MainMenu
from mosaic.widgets.status_bar import StatusBar

_logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(
        self, main_menu: MainMenu, status_bar: StatusBar, view: GraphicsView, inspector: InspectDockable, parent=None
    ):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.setWindowIcon(icon("fa5s.image"))

        self.setMenuBar(main_menu)
        self.setStatusBar(status_bar)
        self.setCentralWidget(view)

        self.populate_menus()

        self.addDockWidget(Qt.LeftDockWidgetArea, inspector)

    def populate_menus(self):
        menu = self.menuBar()
        if isinstance(menu, MainMenu):
            menu.file.addAction(actions.Quit(self))
