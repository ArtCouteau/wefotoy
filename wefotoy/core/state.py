from __future__ import annotations

from .defs import Direction, Location
from .field import Scalar, Vector
from .mesh import Mesh
from .thermo import Thermodynamics
from .scheme.scheme import NumericalSchemes


class State:
    conservative: ConservativeState
    primitive: PrimitiveState

    def __init__(self, mesh: Mesh, schemes: NumericalSchemes) -> None:
        self.conservative = ConservativeState(mesh)
        self.primitive = PrimitiveState(mesh, schemes)


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

    def zero_(self) -> ConservativeState:
        self.density.zero_()
        self.momentum.zero_()
        for tracer in self.tracers.values():
            tracer.zero_()

        return self


class PrimitiveState:
    velocity: Vector
    pressure: Scalar
    tracers: dict[str, Scalar]
    schemes: NumericalSchemes

    def __init__(self, mesh: Mesh, schemes: NumericalSchemes) -> None:
        self.velocity = Vector(
            mesh.zeros((Location.FACE, Location.CENTER)),
            mesh.zeros((Location.CENTER, Location.FACE))
        )
        self.pressure = mesh.zeros((Location.CENTER, Location.CENTER))
        self.tracers = {
            'potential_temperature': mesh.zeros((Location.CENTER, Location.CENTER))
        }
        self.schemes = schemes

    def update(self, conservative: ConservativeState, thermo: Thermodynamics) -> None:
        self.velocity.x.copy_(
            conservative.momentum.x / self.schemes.interpolator.apply(conservative.density, Direction.X)
        )
        self.velocity.y.copy_(
            conservative.momentum.y / self.schemes.interpolator.apply(conservative.density, Direction.Y)
        )
        self.pressure.copy_(thermo.Exner_equation_of_state(conservative))
        for key, tracer in self.tracers.items():
            tracer.copy_(conservative.tracers[key] / conservative.density)
