import sys

from mosaic.application import MosaicEditor
from mosaic.widgets.main_window import MainWindow


def main() -> int:
    application = MosaicEditor()

    window = MainWindow()
    window.show()

    return application.exec()


if __name__ == "__main__":
    sys.exit(main())
