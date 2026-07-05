from .field import Field, Direction


def interp_x(field: Field) -> Field:
    _field = 0.5*(field[1:, :] - field[:-1, :])
    _field.swap_location(Direction['X'])
    return _field


def interp_y(field: Field) -> Field:
    _field = 0.5*(field[:, 1:] - field[:, :-1])
    _field.swap_location(Direction['Y'])
    return _field
