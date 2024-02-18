import inspect
import logging
from abc import ABC, abstractmethod
from typing import TypeVar, Dict, Any, Type, Set

_logger = logging.getLogger(__name__)

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

    @property
    @abstractmethod
    def aliases(self) -> Set[Type[T]]:
        pass

    @property
    @abstractmethod
    def type(self) -> Type[T]:
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

    def __contains__(self, item):
        return self.contains(item)


class RegistrationImpl(Registration):
    def __init__(self, factory: "FactoryImpl", object_type: Type[T]):
        self._factory = factory
        self._object_type = object_type
        self._aliases: Set[Type[T]] = set()
        self._kwargs: Dict[str, Any] = {}
        self._instance = None

    def with_alias(self, alias: Type[T]) -> "RegistrationImpl":
        if not issubclass(self._object_type, alias):
            raise RegistrationError(
                f"Failed to register alias {alias}, {self._object_type} is not a subclass of {alias}"
            )
        self._aliases.add(alias)
        self._factory.register_alias(self._object_type, alias)
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

        # Inspect signature and remove 'self, *args and **kwargs' from it
        signature = inspect.signature(self._object_type.__init__)
        excluded_params = ["self", "args", "kwargs"]
        trimmed_params = [param for param in signature.parameters.values() if param.name not in excluded_params]
        signature = signature.replace(parameters=trimmed_params)

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

    @property
    def aliases(self) -> Set[Type[T]]:
        return self._aliases

    @property
    def type(self) -> Type[T]:
        return self._object_type


class RegistrationError(ValueError):
    pass


class ResolutionError(ValueError):
    pass


class RemovalError(ValueError):
    pass


class FactoryImpl(Factory):
    def __init__(self):
        self._registrations: Dict[Type[T], RegistrationImpl] = {}
        self._aliases: Dict[Type[T], Type[T]] = {}

    def register(self, object_type: Type[T]) -> RegistrationImpl:
        if object_type in self._registrations.keys():
            raise RegistrationError(f"Type {object_type} is already registered")

        if object_type in self._aliases:
            raise RegistrationError(f"Type {object_type} is already registered as an alias")

        self._registrations[object_type] = RegistrationImpl(self, object_type)

        return self._registrations.get(object_type)

    def resolve(self, object_type: Type[T], **kwargs) -> T:
        resolved_type = self._resolve_alias(object_type)
        registration = self._registrations.get(resolved_type, None)
        if registration is None:
            if resolved_type is object_type:
                raise ResolutionError(f"Type {object_type} is not registered")
            else:
                raise ResolutionError(f"{object_type} resolved to {resolved_type}, which is not registered")

        return registration.resolve(**kwargs)

    def remove(self, object_type: Type[T]) -> None:
        if object_type in self._registrations:
            self._remove_object_registration(object_type)
        elif object_type in self._aliases:
            for registration in self._registrations.values():
                if object_type in registration.aliases:
                    self._remove_object_registration(registration.type)
                    break
        else:
            raise RemovalError(f"Type {object_type} is not registered")

    def _remove_object_registration(self, object_type: Type[T]) -> None:
        _logger.debug(f"Removing registration for {object_type}")
        registration = self._registrations.pop(object_type)
        for alias in registration.aliases:
            self._remove_object_alias(alias)

    def _remove_object_alias(self, alias_type: Type[T]) -> None:
        _logger.debug(f"Removing alias {alias_type}")
        self._aliases.pop(alias_type)

    def contains(self, item: Type[T]) -> bool:
        return item in self._registrations or item in self._aliases

    def _resolve_alias(self, alias_type: Type[T]) -> Type[T]:
        if alias_type in self._aliases:
            return self._resolve_alias(self._aliases[alias_type])
        else:
            return alias_type

    def register_alias(self, object_type: Type[T], alias_type: Type[T]) -> None:
        assert issubclass(object_type, alias_type)
        self._aliases[alias_type] = object_type
