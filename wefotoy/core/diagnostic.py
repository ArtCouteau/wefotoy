from .defs import Direction
from .field import Scalar, Vector
from .mesh import Mesh
from .scheme.scheme import NumericalSchemes


def velocity_norm(velocity: Vector, mesh: Mesh, schemes: NumericalSchemes) -> Scalar:
    return kinetic_energy(velocity, mesh, schemes).sqrt_().mul_(2.0)


def kinetic_energy(velocity: Vector, mesh: Mesh, schemes: NumericalSchemes) -> Scalar:
    return (
        schemes.interpolator.apply(velocity.x, Direction.X).interior(mesh).pow_(2)
        + schemes.interpolator.apply(velocity.y, Direction.Y).interior(mesh).pow_(2)
    ).mul_(0.5)
