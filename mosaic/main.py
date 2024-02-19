import sys

import mosaic.widgets as widgets
from mosaic.application import MosaicEditor
from mosaic.widgets.main_window import MainWindow


def main() -> int:
    application = MosaicEditor()

    window = widgets.build(MainWindow)
    window.show()

    return application.exec()


if __name__ == "__main__":
    sys.exit(main())
