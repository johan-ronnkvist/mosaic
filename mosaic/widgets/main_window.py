from PySide6.QtWidgets import QMainWindow, QMenuBar


class MainWindow(QMainWindow):
    def __init__(self, main_menu: QMenuBar, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)

        self.setMenuBar(main_menu)
