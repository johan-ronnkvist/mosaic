import sys

from mosaic.application import MosaicEditor
from mosaic.widgets.main_menu import MainMenu
from mosaic.widgets.main_window import MainWindow
from mosaic.widgets.status_bar import StatusBar


def main() -> int:
    application = MosaicEditor()

    window = MainWindow(MainMenu(), StatusBar())
    window.show()

    return application.exec()


if __name__ == "__main__":
    sys.exit(main())
