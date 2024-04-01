import logging
import sys

import mosaic.widgets as widgets
from mosaic import config
from mosaic.application import MosaicEditor
from mosaic.core.builder import LazyInit
from mosaic.domain.tilescene import TileScene
from mosaic.widgets.main_menu import MainMenu
from mosaic.widgets.main_window import MainWindow
from mosaic.widgets.scene_view import SceneView
from mosaic.widgets.status_bar import StatusBar

logging.basicConfig(level=logging.DEBUG)


def register_widgets():
    factory = widgets.factory
    factory.register(MainMenu, instance=LazyInit)
    factory.register(StatusBar, instance=LazyInit)
    factory.register(MainWindow, instance=LazyInit)
    factory.register(SceneView)
    factory.register(TileScene, instance=TileScene())


def main() -> int:
    application = MosaicEditor()

    config.populate_builder(widgets.factory)

    window = widgets.resolve(widgets.MainWindow)
    window.show()

    return application.exec()


if __name__ == "__main__":
    sys.exit(main())
