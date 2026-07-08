from __future__ import annotations

from ..field import Scalar, Direction
from .interpolation import LinearInterpolator


class Reconstructor:
    velocity: ReconstructorScheme
    scalar: ReconstructorScheme

    def __init__(self) -> None:
        self.velocity = LinearInterpolationReconstructor()
        self.scalar = LinearInterpolationReconstructor()


class ReconstructorScheme:
    halo: int

    def apply(self, advected: Scalar, advecting: Scalar, direction: Direction) -> Scalar: ...


class LinearInterpolationReconstructor(ReconstructorScheme):
    interpolator: LinearInterpolator

    def __init__(self) -> None:
        self.halo = 1
        self.interpolator = LinearInterpolator()

    def apply(self, advected: Scalar, advecting: Scalar, direction: Direction) -> Scalar:
        return self.interpolator.apply(advected, direction)


class UpwindReconstruct(ReconstructorScheme):
    def __init__(self) -> None:
        self.halo = 1

    def apply(self, advected: Scalar, advecting: Scalar, direction: Direction) -> Scalar:
        return advected.left(direction).where(advecting > 0.0, advected.right(direction))
