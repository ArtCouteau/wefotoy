from __future__ import annotations

from ..field import Scalar, Direction


class Interpolator:
    halo: int

    def apply(self, field: Scalar, direction: Direction) -> Scalar: ...


class LinearInterpolator(Interpolator):
    def __init__(self) -> None:
        self.halo = 1

    def apply(self, field: Scalar, direction: Direction) -> Scalar:
        _field = 0.5 * (field.right(direction) + field.left(direction))
        _field.shift_location_and_region(direction)
        return _field
