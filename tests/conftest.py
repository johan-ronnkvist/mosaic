import pytest
from PySide6.QtWidgets import QWidget

from mosaic.widgets.factory import FactoryImpl, Factory


@pytest.fixture
def widget_factory() -> Factory[QWidget]:
    return FactoryImpl[QWidget]()
