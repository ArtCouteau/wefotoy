from __future__ import annotations

from .defs import Location
from .field import Scalar, Vector
from .mesh import Mesh


class ConservativeState:
    density: Scalar
    velocity: Vector
    tracers: dict[str, Scalar]

    def __init__(self, mesh: Mesh) -> None:
        self.density = mesh.zeros((Location.CENTER, Location.CENTER))
