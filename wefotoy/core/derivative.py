from .field import Scalar, Vector, Matrix, Direction
from .mesh import mesh


def _ddx(field: Scalar) -> Scalar:
    _derivative = (field.left(Direction.X) - field.right(Direction.X)) / mesh.dx
    _derivative.swap_location(Direction['X'])
    return _derivative


def _ddy(field: Scalar) -> Scalar:
    _derivative = (field.left(Direction.Y) - field.right(Direction.Y)) / mesh.dy
    _derivative.swap_location(Direction['Y'])
    return _derivative


def divergence_vector(field: Vector) -> Scalar:
    return _ddx(field.x) + _ddy(field.y)


def divergence_matrix(field: Matrix) -> Vector:
    return Vector(divergence_vector(field.x), divergence_vector(field.y))


def gradient_scalar(field: Scalar) -> Vector:
    return (Vector(_ddx(field), _ddy(field)))
