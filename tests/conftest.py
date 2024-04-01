import pytest

from mosaic.core.builder import Builder


@pytest.fixture
def builder() -> Builder:
    return Builder()
