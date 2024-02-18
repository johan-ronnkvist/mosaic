from PySide6.QtWidgets import QMainWindow, QMenuBar, QStatusBar

from mosaic import actions
from mosaic.widgets.main_menu import MainMenu


class MainWindow(QMainWindow):
    def __init__(self, main_menu: QMenuBar, status_bar: QStatusBar, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)

        self.setMenuBar(main_menu)
        self.setStatusBar(status_bar)

        self.populate_menus()

    def populate_menus(self):
        menu = self.menuBar()
        if isinstance(menu, MainMenu):
            menu.file.addAction(actions.Quit(self))
