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
            'potential_temperature_density': mesh.zeros((Location.CENTER, Location.CENTER))
        }
