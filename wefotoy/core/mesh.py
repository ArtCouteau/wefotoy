from __future__ import annotations

from .field import Scalar, Vector, Matrix, Direction


class Mesh:
    N: int = 20
    NGhost: int = 1
    L: float = 1.0
    dx: float
    dy: float

    def __init__(self) -> None:
        self.dx = self.dy = self.L/self.N

    def _ddx(self, field: Scalar) -> Scalar:
        _derivative = (field.left(Direction.X) - field.right(Direction.X)) / self.dx
        _derivative.swap_location(Direction['X'])
        return _derivative

    def _ddy(self, field: Scalar) -> Scalar:
        _derivative = (field.left(Direction.Y) - field.right(Direction.Y)) / self.dy
        _derivative.swap_location(Direction['Y'])
        return _derivative

    def divergence_vector(self, field: Vector) -> Scalar:
        return self._ddx(field.x) + self._ddy(field.y)

    def divergence_matrix(self, field: Matrix) -> Vector:
        return Vector(self.divergence_vector(field.x), self.divergence_vector(field.y))

    def gradient_scalar(self, field: Scalar) -> Vector:
        return Vector(self._ddx(field), self._ddy(field))
