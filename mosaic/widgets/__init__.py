from typing import TypeVar, Type

from PySide6.QtWidgets import QWidget

from mosaic.core.builder import Builder
from .graphics_view import GraphicsView
from .inspector import Inspector, InspectDockable

# flake8: noqa
from .main_menu import MainMenu
from .main_window import MainWindow
from .status_bar import StatusBar

factory: Builder = Builder()

T = TypeVar("T", bound=QWidget)


def resolve(widget_type: Type[T], **kwargs) -> T:
    return factory.resolve(widget_type, **kwargs)
