import pytest

from mosaic.core.factory import FactoryImpl, Factory


@pytest.fixture
def factory() -> Factory:
    return FactoryImpl()
