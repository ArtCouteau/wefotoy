from __future__ import annotations

from .defs import Location
from .field import Scalar, Vector
from .mesh import Mesh


class ConservativeState:
    density: Scalar
    momentum: Vector
    tracers: dict[str, Scalar]

    def __init__(self, mesh: Mesh) -> None:
        self.density = mesh.zeros((Location.CENTER, Location.CENTER))
        self.momentum = Vector(
            mesh.zeros((Location.FACE, Location.CENTER)),
            mesh.zeros((Location.CENTER, Location.FACE))
        )
        self.tracers = {
            'potential_temperature': mesh.zeros((Location.CENTER, Location.CENTER))
        }

    def add_(self, other: ConservativeState) -> ConservativeState:
        self.density.add_(other.density)
        self.momentum.add_(other.momentum)
        for key, tracer in self.tracers.items():
            tracer.add_(other.tracers[key])

        return self

    def mul_(self, other: int | float) -> ConservativeState:
        self.density.mul_(other)
        self.momentum.mul_(other)
        for tracer in self.tracers.values():
            tracer.mul_(other)

        return self


class PrimitiveState:
    velocity: Vector
    pressure: Scalar
    tracers: dict[str, Scalar]

    def __init__(self, mesh: Mesh) -> None:
        self.velocity = Vector(
            mesh.zeros((Location.FACE, Location.CENTER)),
            mesh.zeros((Location.CENTER, Location.FACE))
        )
        self.pressure = mesh.zeros((Location.CENTER, Location.CENTER))
        self.tracers = {
            'potential_temperature': mesh.zeros((Location.CENTER, Location.CENTER))
        }
