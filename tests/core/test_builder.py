from typing import List

import pytest

from mosaic.core.builder import Builder, ResolutionError, RegistrationError, RemovalError


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


class TestBuilder:
    def test_register_unknown_type(self, builder: Builder):
        builder.register(Camera)
        assert builder.contains(Camera)

    def test_resolve_registered_type(self, builder: Builder):
        builder.register(Camera)
        item = builder.resolve(Camera)
        assert isinstance(item, Camera)

    def test_resolve_type_with_kwargs(self, builder: Builder):
        builder.register(Texture)
        item = builder.resolve(Texture, filename="texture.png")
        assert isinstance(item, Texture)
        assert item.filename == "texture.png"

    def test_resolve_type_with_missing_dependency_raises_error(self, builder: Builder):
        builder.register(Viewport)
        with pytest.raises(ResolutionError):
            builder.resolve(Viewport)

    def test_resolve_type_with_existing_dependency(self, builder: Builder):
        builder.register(Camera)
        builder.register(Viewport)
        viewport = builder.resolve(Viewport)
        assert isinstance(viewport, Viewport)
        assert viewport.camera is not None

    def test_register_type_with_provided_kwargs(self, builder: Builder):
        builder.register(Texture).with_kwargs(filename="texture.png")
        texture = builder.resolve(Texture)
        assert isinstance(texture, Texture)
        assert texture.filename == "texture.png"

    def test_resolve_type_with_provided_instance(self, builder: Builder):
        camera = Camera()
        builder.register(Camera).with_instance(camera)
        builder.register(Viewport)
        viewport = builder.resolve(Viewport)
        assert viewport.camera is camera

    def test_register_instance_with_kwargs_raises_error(self, builder: Builder):
        texture = Texture("texture.png")
        with pytest.raises(RegistrationError):
            builder.register(Texture).with_instance(texture).with_kwargs(filename="other.png")

    def test_register_kwargs_for_instance_raises_error(self, builder: Builder):
        texture = Texture("texture.png")
        with pytest.raises(RegistrationError):
            builder.register(Texture).with_kwargs(filename="other.png").with_instance(texture)

    def test_resolve_type_with_alias(self, builder: Builder):
        builder.register(Capsule).with_kwargs(height=2, width=2, depth=2).with_alias(Mesh)
        assert builder.contains(Capsule)
        assert builder.contains(Mesh)

        mesh = builder.resolve(Mesh)
        assert isinstance(mesh, Mesh)
        assert isinstance(mesh, Capsule)
        assert len(mesh.vertices) == 8

        capsule = builder.resolve(Capsule)
        assert isinstance(capsule, Capsule)
        assert isinstance(capsule, Mesh)

    def test_remove_type_also_removes_aliases(self, builder: Builder):
        builder.register(Capsule).with_kwargs(height=2, width=2, depth=2).with_alias(Mesh)
        assert builder.contains(Capsule)
        assert builder.contains(Mesh)

        builder.remove(Capsule)
        assert not builder.contains(Capsule)
        assert not builder.contains(Mesh)

    def test_remove_alias_also_removes_type(self, builder: Builder):
        builder.register(Capsule).with_kwargs(height=2, width=2, depth=2).with_alias(Mesh)
        assert builder.contains(Capsule)
        assert builder.contains(Mesh)

        builder.remove(Mesh)
        assert not builder.contains(Capsule)
        assert not builder.contains(Mesh)

    def test_register_type_with_invalid_alias(self, builder: Builder):
        with pytest.raises(RegistrationError):
            builder.register(Texture).with_alias(str)

    def test_resolve_with_kwargs_for_instance(self, builder: Builder):
        texture = Texture("texture.png")
        builder.register(Texture).with_instance(texture)
        with pytest.raises(ResolutionError):
            builder.resolve(Texture, filename="other.png")

    def test_register_existing_type_raises_error(self, builder: Builder):
        builder.register(Texture)
        with pytest.raises(RegistrationError):
            builder.register(Texture)

    def test_register_type_that_is_already_registered_as_alias_raises_error(self, builder: Builder):
        builder.register(Capsule).with_alias(Mesh)
        with pytest.raises(RegistrationError):
            builder.register(Mesh)

    def test_remove_unregistered_type_raises_error(self, builder: Builder):
        assert not builder.contains(Texture)
        with pytest.raises(RemovalError):
            builder.remove(Texture)

    def test_resolve_type_with_multiple_dependencies(self, builder: Builder):
        builder.register(Mesh).with_kwargs(vertices=[Vertex()])
        builder.register(Texture).with_kwargs(filename="texture.png")
        builder.register(Model)
        first = builder.resolve(Model)
        assert isinstance(first, Model)
        assert first.texture.filename == "texture.png"

        second = builder.resolve(Model, texture=Texture("other.png"))
        assert isinstance(second, Model)
        assert second.texture.filename == "other.png"
