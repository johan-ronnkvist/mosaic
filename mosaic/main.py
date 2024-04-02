import logging
import sys

import mosaic.widgets as widgets
from mosaic import config
from mosaic.application import MosaicEditor

logging.basicConfig(level=logging.DEBUG)


def main() -> int:
    application = MosaicEditor()

    config.populate_builder(widgets.factory)

    window = widgets.resolve(widgets.MainWindow)
    window.show()

    return application.exec()


if __name__ == "__main__":
    sys.exit(main())
