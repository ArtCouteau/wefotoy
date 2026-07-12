from .defs import Direction
from .field import Scalar, Vector
from .scheme.scheme import NumericalSchemes


def velocity_norm(velocity: Vector, schemes: NumericalSchemes) -> Scalar:
    return (
        schemes.interpolator.apply(velocity.x, Direction.X).pow_(2)
        + schemes.interpolator.apply(velocity.y, Direction.Y).pow_(2)
    ).sqrt_()


def kinetic_energy(velocity: Vector, schemes: NumericalSchemes) -> Scalar:
    return (
        schemes.interpolator.apply(velocity.x, Direction.X).pow_(2)
        + schemes.interpolator.apply(velocity.y, Direction.Y).pow_(2)
    ).mul_(0.5)
