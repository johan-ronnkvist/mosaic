import pytest
from PySide6.QtWidgets import QWidget

from mosaic.widgets.factory import Factory, ResolutionError, RegistrationError, RemovalError


class Widget1(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


class Widget2(Widget1):
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.text = text


class Widget3(QWidget):
    def __init__(self, widget1: Widget1, parent=None):
        super().__init__(parent)
        self.widget1 = widget1


class TestWidgetFactory:
    def test_register_type(self, widget_factory: Factory):
        widget_factory.register(Widget1)
        assert widget_factory.contains(Widget1)

    def test_resolve_type(self, qtbot, widget_factory: Factory):
        widget_factory.register(Widget1)
        widget = widget_factory.resolve(Widget1)
        assert isinstance(widget, Widget1)

    def test_resolve_type_with_kwargs(self, qtbot, widget_factory: Factory):
        widget_factory.register(Widget2)
        widget = widget_factory.resolve(Widget2, text="Hello World")
        assert isinstance(widget, Widget2)
        assert widget.text == "Hello World"

    def test_resolve_type_with_missing_dependency_raises_error(self, qtbot, widget_factory: Factory):
        widget_factory.register(Widget3)
        with pytest.raises(ResolutionError):
            widget_factory.resolve(Widget3)

    def test_resolve_type_with_existing_dependency(self, qtbot, widget_factory: Factory):
        widget_factory.register(Widget1)
        widget_factory.register(Widget3)
        widget1 = widget_factory.resolve(Widget1)
        widget = widget_factory.resolve(Widget3, widget1=widget1)
        assert isinstance(widget, Widget3)
        assert widget.widget1 == widget1

    def test_register_type_with_provided_kwargs(self, qtbot, widget_factory: Factory):
        widget_factory.register(Widget2).with_kwargs(text="Hello World")
        widget = widget_factory.resolve(Widget2)
        assert isinstance(widget, Widget2)
        assert widget.text == "Hello World"

    def test_resolve_type_with_provided_instance(self, qtbot, widget_factory: Factory):
        widget = Widget2("Hello World")
        widget_factory.register(Widget2).with_instance(widget)
        resolved_widget = widget_factory.resolve(Widget2)
        assert resolved_widget is widget
        assert resolved_widget.text == "Hello World"

    def test_register_instance_with_kwargs_raises_error(self, qtbot, widget_factory: Factory):
        widget = Widget2("Hello World")
        with pytest.raises(RegistrationError):
            widget_factory.register(Widget2).with_instance(widget).with_kwargs(text="Goodbye World")

    def test_register_kwargs_for_instance_raises_error(self, qtbot, widget_factory: Factory):
        widget = Widget2("Hello World")
        with pytest.raises(RegistrationError):
            widget_factory.register(Widget2).with_kwargs(text="Goodbye World").with_instance(widget)

    def test_resolve_type_with_alias(self, qtbot, widget_factory: Factory):
        widget_factory.register(Widget2).with_kwargs(text="Hello World").with_alias(Widget1)
        assert widget_factory.contains(Widget1)
        assert widget_factory.contains(Widget2)
        widget1 = widget_factory.resolve(Widget1)
        assert isinstance(widget1, Widget1)
        assert isinstance(widget1, Widget2)
        assert widget1.text == "Hello World"
        widget2 = widget_factory.resolve(Widget2)
        assert isinstance(widget2, Widget2)

    def test_remove_type_also_removes_aliases(self, qtbot, widget_factory: Factory):
        widget_factory.register(Widget2).with_kwargs(text="Hello World").with_alias(Widget1)
        widget_factory.remove(Widget2)
        assert not widget_factory.contains(Widget1)
        assert not widget_factory.contains(Widget2)

    def test_remove_alias_also_removes_type(self, qtbot, widget_factory: Factory):
        widget_factory.register(Widget2).with_kwargs(text="Hello World").with_alias(Widget1)
        widget_factory.remove(Widget1)
        assert not widget_factory.contains(Widget1)
        assert not widget_factory.contains(Widget2)
        assert Widget2 not in widget_factory

    def test_register_type_with_invalid_alias(self, qtbot, widget_factory: Factory):
        with pytest.raises(RegistrationError):
            widget_factory.register(Widget1).with_alias(str)

    def test_resolve_with_kwargs_for_instance(self, qtbot, widget_factory: Factory):
        widget = Widget2("Hello World")
        widget_factory.register(Widget2).with_instance(widget)
        with pytest.raises(ResolutionError):
            widget_factory.resolve(Widget2, text="Goodbye World")

    def test_register_existing_type_raises_error(self, qtbot, widget_factory: Factory):
        widget_factory.register(Widget1)
        with pytest.raises(RegistrationError):
            widget_factory.register(Widget1)

    def test_register_type_that_is_already_registered_as_alias_raises_error(self, qtbot, widget_factory: Factory):
        widget_factory.register(Widget2).with_alias(Widget1)
        with pytest.raises(RegistrationError):
            widget_factory.register(Widget1)

    def test_remove_unregistered_type_raises_error(self, qtbot, widget_factory: Factory):
        assert not widget_factory.contains(Widget1)
        with pytest.raises(RemovalError):
            widget_factory.remove(Widget1)
