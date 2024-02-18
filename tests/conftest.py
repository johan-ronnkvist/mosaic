import pytest

from mosaic.widgets.factory import FactoryImpl, Factory


@pytest.fixture
def widget_factory() -> Factory:
    return FactoryImpl()
