from .field import Scalar, Direction


def interp_x(field: Scalar) -> Scalar:
    _field = 0.5*(field[1:, :] - field[:-1, :])
    _field.swap_location(Direction['X'])
    return _field


def interp_y(field: Scalar) -> Scalar:
    _field = 0.5*(field[:, 1:] - field[:, :-1])
    _field.swap_location(Direction['Y'])
    return _field
