from PySide6.QtWidgets import QWidget

from mosaic.widgets.factory import Factory


class CustomWidget1(QWidget):
    pass


class CustomWidget2(QWidget):
    pass


# class TestFactory:
def test_register_type(self, widget_factory: Factory[QWidget]):
    widget_factory.register(CustomWidget1)
