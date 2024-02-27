import sys

from mosaic import widgets, config
from mosaic.application import MosaicEditor


def main() -> int:
    application = MosaicEditor()

    config.populate_builder(widgets.factory)

    window = widgets.resolve(widgets.MainWindow)
    window.show()

    return application.exec()


if __name__ == "__main__":
    sys.exit(main())
