from typing import TypeVar, Type

from PySide6.QtWidgets import QWidget

from mosaic.core.builder import BuilderImpl, Builder

factory: Builder = BuilderImpl()

T = TypeVar("T", bound=QWidget)


def build(widget_type: Type[T], *args, **kwargs) -> T:
    return factory.resolve(widget_type, *args, **kwargs)
