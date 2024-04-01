from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication


class Quit(QAction):
    def __init__(self, parent=None):
        super(Quit, self).__init__(parent)
        self.setText("Quit")
        self.setStatusTip("Quit the application")
        self.triggered.connect(QApplication.quit)
