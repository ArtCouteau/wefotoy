from .field import Scalar, Direction


def linear(field: Scalar, direction: Direction) -> Scalar:
    _field = 0.5 * (field.right(direction) + field.left(direction))
    _field.swap_location(direction)
    return _field
