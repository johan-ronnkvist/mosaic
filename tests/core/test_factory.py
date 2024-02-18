from typing import List

import pytest

from mosaic.core.factory import Factory, ResolutionError, RegistrationError, RemovalError


class Component:
    pass


class Camera(Component):
    pass


class Vertex:
    pass


class Viewport:
    def __init__(self, camera: Camera):
        self.camera = camera


class Mesh(Component):
    def __init__(self, vertices: List[Vertex]):
        self.vertices = vertices


class Capsule(Mesh):
    def __init__(self, height: int, width: int, depth: int):
        super().__init__(self.compute_mesh(height, width, depth))

    @staticmethod
    def compute_mesh(height: int, width: int, depth: int) -> List[Vertex]:
        return [Vertex() for _ in range(height * width * depth)]


class Texture(Component):
    def __init__(self, filename: str):
        self.filename = filename


class Model(Component):
    def __init__(self, mesh: Mesh, texture: Texture):
        self.mesh = mesh
        self.texture = texture


class TestWidgetFactory:
    def test_register_type(self, factory: Factory):
        factory.register(Camera)
        assert factory.contains(Camera)

    def test_resolve_type(self, factory: Factory):
        factory.register(Camera)
        item = factory.resolve(Camera)
        assert isinstance(item, Camera)

    def test_resolve_type_with_kwargs(self, factory: Factory):
        factory.register(Texture)
        item = factory.resolve(Texture, filename="texture.png")
        assert isinstance(item, Texture)
        assert item.filename == "texture.png"

    def test_resolve_type_with_missing_dependency_raises_error(self, factory: Factory):
        factory.register(Viewport)
        with pytest.raises(ResolutionError):
            factory.resolve(Viewport)

    def test_resolve_type_with_existing_dependency(self, factory: Factory):
        factory.register(Camera)
        factory.register(Viewport)
        viewport = factory.resolve(Viewport)
        assert isinstance(viewport, Viewport)
        assert viewport.camera is not None

    def test_register_type_with_provided_kwargs(self, factory: Factory):
        factory.register(Texture).with_kwargs(filename="texture.png")
        texture = factory.resolve(Texture)
        assert isinstance(texture, Texture)
        assert texture.filename == "texture.png"

    def test_resolve_type_with_provided_instance(self, factory: Factory):
        camera = Camera()
        factory.register(Camera).with_instance(camera)
        factory.register(Viewport)
        viewport = factory.resolve(Viewport)
        assert viewport.camera is camera

    def test_register_instance_with_kwargs_raises_error(self, factory: Factory):
        texture = Texture("texture.png")
        with pytest.raises(RegistrationError):
            factory.register(Texture).with_instance(texture).with_kwargs(filename="other.png")

    def test_register_kwargs_for_instance_raises_error(self, factory: Factory):
        texture = Texture("texture.png")
        with pytest.raises(RegistrationError):
            factory.register(Texture).with_kwargs(filename="other.png").with_instance(texture)

    def test_resolve_type_with_alias(self, factory: Factory):
        factory.register(Capsule).with_kwargs(height=2, width=2, depth=2).with_alias(Mesh)
        assert factory.contains(Capsule)
        assert factory.contains(Mesh)

        mesh = factory.resolve(Mesh)
        assert isinstance(mesh, Mesh)
        assert isinstance(mesh, Capsule)
        assert len(mesh.vertices) == 8

        capsule = factory.resolve(Capsule)
        assert isinstance(capsule, Capsule)
        assert isinstance(capsule, Mesh)

    def test_remove_type_also_removes_aliases(self, factory: Factory):
        factory.register(Capsule).with_kwargs(height=2, width=2, depth=2).with_alias(Mesh)
        assert factory.contains(Capsule)
        assert factory.contains(Mesh)

        factory.remove(Capsule)
        assert not factory.contains(Capsule)
        assert not factory.contains(Mesh)

    def test_remove_alias_also_removes_type(self, factory: Factory):
        factory.register(Capsule).with_kwargs(height=2, width=2, depth=2).with_alias(Mesh)
        assert factory.contains(Capsule)
        assert factory.contains(Mesh)

        factory.remove(Mesh)
        assert not factory.contains(Capsule)
        assert not factory.contains(Mesh)

    def test_register_type_with_invalid_alias(self, factory: Factory):
        with pytest.raises(RegistrationError):
            factory.register(Texture).with_alias(str)

    def test_resolve_with_kwargs_for_instance(self, factory: Factory):
        texture = Texture("texture.png")
        factory.register(Texture).with_instance(texture)
        with pytest.raises(ResolutionError):
            factory.resolve(Texture, filename="other.png")

    def test_register_existing_type_raises_error(self, factory: Factory):
        factory.register(Texture)
        with pytest.raises(RegistrationError):
            factory.register(Texture)

    def test_register_type_that_is_already_registered_as_alias_raises_error(self, factory: Factory):
        factory.register(Capsule).with_alias(Mesh)
        with pytest.raises(RegistrationError):
            factory.register(Mesh)

    def test_remove_unregistered_type_raises_error(self, factory: Factory):
        assert not factory.contains(Texture)
        with pytest.raises(RemovalError):
            factory.remove(Texture)

    def test_resolve_type_with_multiple_dependencies(self, factory: Factory):
        factory.register(Mesh).with_kwargs(vertices=[Vertex()])
        factory.register(Texture).with_kwargs(filename="texture.png")
        factory.register(Model)
        first = factory.resolve(Model)
        assert isinstance(first, Model)
        assert first.texture.filename == "texture.png"

        second = factory.resolve(Model, texture=Texture("other.png"))
        assert isinstance(second, Model)
        assert second.texture.filename == "other.png"
