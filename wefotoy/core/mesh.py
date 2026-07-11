from __future__ import annotations

import torch

from .defs import AxisLocation, Location, Side
from .field import Scalar, Vector, Matrix, Direction


class Mesh:
    N: int = 20
    NGhost: int = 1
    L: float = 1.0
    dx: float
    dy: float
    interior: dict[AxisLocation, slice]
    boundary: dict[Side, slice]

    def __init__(self) -> None:
        self.dx = self.dy = self.L/self.N
        self.interior = {
            AxisLocation.CENTER: slice(self.NGhost, -self.NGhost),
            AxisLocation.FACE: slice(None),
        }
        self.boundary = {
            Side.LOWER: slice(0, self.NGhost),
            Side.UPPER: slice(-self.NGhost, None)
        }

    def _ddx(self, field: Scalar) -> Scalar:
        _derivative = (field.right(Direction.X) - field.left(Direction.X)) / self.dx
        _derivative.swap_location(Direction['X'])
        return _derivative

    def _ddy(self, field: Scalar) -> Scalar:
        _derivative = (field.right(Direction.Y) - field.left(Direction.Y)) / self.dy
        _derivative.swap_location(Direction['Y'])
        return _derivative

    def divergence_vector(self, field: Vector) -> Scalar:
        return self._ddx(field.x) + self._ddy(field.y)

    def divergence_matrix(self, field: Matrix) -> Vector:
        return Vector(self.divergence_vector(field.x), self.divergence_vector(field.y))

    def gradient_scalar(self, field: Scalar) -> Vector:
        return Vector(self._ddx(field), self._ddy(field))

    def zeros(self, location: Location) -> Scalar:
        size: list[int] = []
        for direction in Direction:
            if location[direction] is AxisLocation.CENTER:
                size.append(self.N + 2*self.NGhost)
            else:
                size.append(self.N + 1)

        return Scalar(torch.zeros(size), location)
