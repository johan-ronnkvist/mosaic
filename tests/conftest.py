import pytest

from mosaic.core.builder import BuilderImpl, Builder


@pytest.fixture
def builder() -> Builder:
    return BuilderImpl()
