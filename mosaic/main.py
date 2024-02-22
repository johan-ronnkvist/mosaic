import sys

import mosaic.widgets as widgets
from mosaic.application import MosaicEditor
from mosaic.widgets.main_menu import MainMenu
from mosaic.widgets.main_window import MainWindow
from mosaic.widgets.status_bar import StatusBar


def register_widgets():
    factory = widgets.factory
    factory.register(MainMenu, instance=MainMenu())
    factory.register(StatusBar, instance=StatusBar())


def main() -> int:
    application = MosaicEditor()

    register_widgets()

    window = widgets.resolve(MainWindow)
    window.show()

    return application.exec()


if __name__ == "__main__":
    sys.exit(main())
