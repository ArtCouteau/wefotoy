from __future__ import annotations

from .defs import Direction, Side
from .field import Scalar
from .mesh import Mesh


class BoundaryCondition:
    direction: Direction
    side: Side

    def __init__(self, direction: Direction, side: Side) -> None:
        self.direction = direction
        self.side = side

    def apply(self, field: Scalar, mesh: Mesh) -> None: ...


class Periodic(BoundaryCondition):
    def apply(self, field: Scalar, mesh: Mesh) -> None:
        field.boundary(self.direction, self.side, mesh).data = field.adjacent(
            self.direction, self.side.opposite(), mesh
        ).data


class FixedFlux(BoundaryCondition):
    flux: float

    def __init__(self, direction: Direction, side: Side, flux: float) -> None:
        super().__init__(direction, side)
        self.flux = flux

    def apply(self, field: Scalar, mesh: Mesh) -> None:
        field.boundary(self.direction, self.side, mesh).copy_(
            field.adjacent(self.direction, self.side, mesh)
        ).add_(self.flux)


class ZeroGradient(FixedFlux):
    def __init__(self, direction: Direction, side: Side) -> None:
        super().__init__(direction, side, flux=0.0)
