from .defs import Direction
from .field import Scalar, Vector, Matrix
from .mesh import Mesh


def _ddx(field: Scalar, mesh: Mesh) -> Scalar:
    _derivative = (field.right(Direction.X) - field.left(Direction.X)) / mesh.dx
    _derivative.shift_location_and_region(Direction['X'])
    return _derivative


def _ddy(field: Scalar, mesh: Mesh) -> Scalar:
    _derivative = (field.right(Direction.Y) - field.left(Direction.Y)) / mesh.dy
    _derivative.shift_location_and_region(Direction['Y'])
    return _derivative


def divergence_vector(field: Vector, mesh: Mesh) -> Scalar:
    return _ddx(field.x, mesh).add_(_ddy(field.y, mesh))


def divergence_matrix(field: Matrix, mesh: Mesh) -> Vector:
    return Vector(divergence_vector(field.x, mesh), divergence_vector(field.y, mesh))


def gradient_scalar(field: Scalar, mesh: Mesh) -> Vector:
    return Vector(_ddx(field, mesh), _ddy(field, mesh))
