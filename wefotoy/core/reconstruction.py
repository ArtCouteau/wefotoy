from __future__ import annotations

from .field import Scalar, Direction
from . import interpolation


class Reconstructor:
    halo: int

    def apply(self, advected: Scalar, advecting: Scalar, direction: Direction) -> Scalar: ...


class LinearInterpolationReconstructor(Reconstructor):
    def __init__(self) -> None:
        self.halo = 1

    def apply(self, advected: Scalar, advecting: Scalar, direction: Direction) -> Scalar:
        return interpolation.linear(advected, direction)


class UpwindReconstruct(Reconstructor):
    def __init__(self) -> None:
        self.halo = 1

    def apply(self, advected: Scalar, advecting: Scalar, direction: Direction) -> Scalar:
        return advected.left(direction).where(advecting > 0.0, advected.right(direction))
