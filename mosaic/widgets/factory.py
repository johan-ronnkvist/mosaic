from typing import Protocol, TypeVar, Generic, Dict

from PySide6.QtWidgets import QWidget

T = TypeVar("T", bound=QWidget)


class Factory(Protocol[T]):
    def register(self, object_type: type[T]) -> "Registration": ...

    def resolve(self, object_type: type[T], *args, **kwargs) -> T: ...


class Registration(Protocol[T]):
    def with_alias(self, alias: type[T]) -> "Registration": ...

    def using_instance(self, widget: T) -> "Registration": ...

    def resolve(self, factory: Factory[T], *args, **kwargs) -> T: ...


class RegistrationImpl(Generic[T]):
    def __init__(self, factory: Factory[T], object_type: type[T]):
        self._factory = factory
        self._object_type = object_type
        self._aliases = set()
        self._instance = None

    def with_alias(self, alias: type[T]) -> "Registration":
        self._aliases.add(alias)
        # TODO: alias must be registered in factory also...
        return self

    def using_instance(self, instance: T) -> "Registration":
        self._instance = instance
        return self

    def resolve(self, *args, **kwargs) -> T:
        if self._instance is not None:
            # TODO: warn if args or kwargs are not empty
            return self._instance

        return self._object_type(*args, **kwargs)


class RegistrationError(ValueError):
    pass


class ResolutionError(ValueError):
    pass


class FactoryImpl(Generic[T]):
    def __init__(self):
        self._registrations = Dict[type[T], Registration[T]]()

    def register(self, object_type: type[T]) -> Registration[T]:
        if self._registrations.get(object_type) is not None:
            raise RegistrationError(f"Type {object_type} is already registered")

        self._registrations[object_type] = RegistrationImpl[T](self, object_type)

        return self._registrations[object_type]

    def resolve(self, object_type: type[T], *args, **kwargs) -> T:
        registration = self._registrations.get(object_type)
        if registration is None:
            raise ResolutionError(f"Type {object_type} is not registered")

        return registration.resolve(*args, **kwargs)


widget_factory = FactoryImpl[T]()

"""
Usage Example:
factory = WidgetFactory()

single_main_menu = MyMenuBar()

factory.register_type(MyMenuBar).as_type(QMenuBar).using_instance(single_main_menu)

menu = factory.get(QMenuBar)
assert menu is single_main_menu
assert isinstance(menu, MyMenuBar)


"""
