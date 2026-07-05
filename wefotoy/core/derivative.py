from .field import Field, Direction
from .mesh import mesh


def ddx(field: Field) -> Field:
    _field = (field[1:, :] - field[:-1, :])/mesh.dx
    _field.swap_location(Direction['X'])
    return _field


def ddy(field: Field) -> Field:
    _field = (field[:, 1:] - field[:, :-1])/mesh.dy
    _field.swap_location(Direction['Y'])
    return _field
