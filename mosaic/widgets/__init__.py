from typing import TypeVar, Type

from PySide6.QtWidgets import QWidget

from mosaic.core.builder import Builder

factory: Builder = Builder()

T = TypeVar("T", bound=QWidget)


def register(**kwargs):
    def decorator(cls):
        factory.register(cls, **kwargs)
        return cls

    return decorator


def resolve(widget_type: Type[T], **kwargs) -> T:
    return factory.resolve(widget_type, **kwargs)
