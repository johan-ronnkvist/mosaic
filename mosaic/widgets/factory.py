import inspect
from abc import ABC, abstractmethod
from typing import TypeVar, Dict, Any, Type

T = TypeVar("T")


class Registration(ABC):
    @abstractmethod
    def with_alias(self, alias: Type[T]) -> "Registration":
        pass

    @abstractmethod
    def with_kwargs(self, **kwargs) -> "Registration":
        pass

    @abstractmethod
    def with_instance(self, widget: T) -> "Registration":
        pass

    @abstractmethod
    def resolve(self, factory: "Factory", *args, **kwargs) -> T:
        pass


class Factory(ABC):
    @abstractmethod
    def register(self, object_type: Type[T]) -> Registration:
        pass

    @abstractmethod
    def resolve(self, object_type: Type[T], *args, **kwargs) -> T:
        pass

    @abstractmethod
    def remove(self, object_type: Type[T]) -> None:
        pass

    @abstractmethod
    def contains(self, object_type: Type[T]) -> bool:
        pass


class RegistrationImpl(Registration):
    def __init__(self, factory: Factory, object_type: Type[T]):
        self._factory = factory
        self._object_type = object_type
        self._aliases = set(Type[T])
        self._instance = None
        self._kwargs: Dict[str, Any] = {}

    def with_alias(self, alias: Type[T]) -> "RegistrationImpl":
        self._aliases.add(alias)
        # TODO: alias must be registered in factory also...
        return self

    def with_kwargs(self, **kwargs) -> "RegistrationImpl":
        if self._instance is not None:
            raise RegistrationError("Cannot provide kwargs when using instance")
        self._kwargs.update(kwargs)
        return self

    def with_instance(self, instance: T) -> "RegistrationImpl":
        if self._kwargs:
            raise RegistrationError("Cannot provide instance when using kwargs")
        self._instance = instance
        return self

    def resolve(self, **kwargs) -> T:
        if self._instance is not None:
            if kwargs:
                raise ResolutionError("Instance is already provided, cannot provide additional kwargs.")
            return self._instance

        # Inspect signature and remove 'self' from it
        signature = inspect.signature(self._object_type.__init__)
        signature = signature.replace(parameters=list(signature.parameters.values())[1:])

        resolved_args = []
        resolved_kwargs = self._kwargs.copy()

        # Resolve parameters in the following order:
        # 1. if a parameter is provided in kwargs, use it.
        # 2. else, if a parameter exists in self._kwargs, use it.
        # 3. else, if a parameter has a default value, use it.
        # 4. else, resolve from factory
        for param in signature.parameters.values():
            if param.name in kwargs:
                resolved_kwargs[param.name] = kwargs[param.name]
            elif param.name in self._kwargs:
                resolved_kwargs[param.name] = self._kwargs[param.name]
            elif param.default != param.empty:
                resolved_kwargs[param.name] = param.default
            else:
                resolved_args.append(self._factory.resolve(param.annotation))

        return self._object_type(*resolved_args, **resolved_kwargs)


class RegistrationError(ValueError):
    pass


class ResolutionError(ValueError):
    pass


class FactoryImpl(Factory):
    def __init__(self):
        self._registrations: Dict[Type[T], RegistrationImpl] = {}

    def register(self, object_type: Type[T]) -> RegistrationImpl:
        if self._registrations.get(object_type) is not None:
            raise RegistrationError(f"Type {object_type} is already registered")

        self._registrations[object_type] = RegistrationImpl(self, object_type)

        return self._registrations[object_type]

    def resolve(self, object_type: Type[T], **kwargs) -> T:
        registration = self._registrations.get(object_type)
        if registration is None:
            raise ResolutionError(f"Type {object_type} is not registered")

        return registration.resolve(**kwargs)

    def remove(self, object_type: Type[T]) -> None:
        self._registrations.pop(object_type, None)

    def contains(self, item: Type[T]) -> bool:
        return item in self._registrations

    def __contains__(self, item) -> bool:
        return self.contains(item)


widget_factory = FactoryImpl()

"""
Usage Example:
factory = WidgetFactory()

single_main_menu = MyMenuBar()

factory.register_type(MyMenuBar).as_type(QMenuBar).using_instance(single_main_menu)

menu = factory.get(QMenuBar)
assert menu is single_main_menu
assert isinstance(menu, MyMenuBar)


"""
