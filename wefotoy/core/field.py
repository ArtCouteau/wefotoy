from __future__ import annotations

import torch

from .defs import Direction, AxisLocation, Location, Side
from .mesh import Mesh


class Field:
    data: torch.Tensor
    location: Location

    def __init__(self, data: torch.Tensor, location: Location) -> None:
        self.data = data
        self.location = location


class Scalar(Field):
    def __init__(self, data: torch.Tensor, location: Location) -> None:
        super().__init__(data, location)

    def __getitem__(self, slices: tuple[slice, ...]) -> Scalar:
        return Scalar(self.data[slices], self.location)

    def __add__(self, other: Scalar) -> Scalar:
        assert (self.location == other.location)
        return Scalar(self.data + other.data, self.location)

    def __sub__(self, other: Scalar) -> Scalar:
        assert (self.location == other.location)
        return Scalar(self.data - other.data, self.location)

    def __neg__(self) -> Scalar:
        return Scalar(-self.data, self.location)

    def __mul__(self, other: int | float | Scalar) -> Scalar:
        if isinstance(other, (int, float)):
            return Scalar(self.data*other, self.location)
        else:
            assert (self.location == other.location)
            return Scalar(self.data*other.data, self.location)

    def __rmul__(self, other: int | float | Scalar) -> Scalar:
        return self.__mul__(other)

    def __truediv__(self, other: int | float | Scalar) -> Scalar:
        if isinstance(other, (int, float)):
            return Scalar(self.data/other, self.location)
        else:
            assert (self.location == other.location)
            return Scalar(self.data/other.data, self.location)

    def __rtruediv__(self, other: int | float | Scalar) -> Scalar:
        return self.__truediv__(other)

    def __gt__(self, other: int | float | Scalar) -> Scalar:
        if isinstance(other, (int, float)):
            return Scalar(self.data > other, self.location)
        else:
            assert (self.location == other.location)
            return Scalar(self.data > other.data, self.location)

    def __lt__(self, other: int | float | Scalar) -> Scalar:
        if isinstance(other, (int, float)):
            return Scalar(self.data < other, self.location)
        else:
            assert (self.location == other.location)
            return Scalar(self.data < other.data, self.location)

    def __ge__(self, other: int | float | Scalar) -> Scalar:
        if isinstance(other, (int, float)):
            return Scalar(self.data >= other, self.location)
        else:
            assert (self.location == other.location)
            return Scalar(self.data >= other.data, self.location)

    def __le__(self, other: int | float | Scalar) -> Scalar:
        if isinstance(other, (int, float)):
            return Scalar(self.data <= other, self.location)
        else:
            assert (self.location == other.location)
            return Scalar(self.data <= other.data, self.location)

    def add_(self, other: Scalar) -> Scalar:
        assert (self.location == other.location)
        self.data.add_(other.data)
        return self

    def mul_(self, other: int | float) -> Scalar:
        self.data.mul_(other)
        return self

    def copy_(self, other: Scalar) -> Scalar:
        assert (self.location == other.location)
        self.data.copy_(other.data)
        return self

    def pow_(self, exponent: float) -> Scalar:
        self.data.pow_(exponent)
        return self

    def sqrt_(self) -> Scalar:
        self.data.sqrt_()
        return self

    def zero_(self) -> Scalar:
        self.data.zero_()
        return self

    def min(self) -> float:
        return self.data.min().item()

    def minimum(self, other: Scalar) -> Scalar:
        assert (self.location == other.location)
        return Scalar(self.data.minimum(other.data), self.location)

    def max(self) -> float:
        return self.data.max().item()

    def maximum(self, other: Scalar) -> Scalar:
        assert (self.location == other.location)
        return Scalar(self.data.maximum(other.data), self.location)

    def where(self, condition: Scalar, other: Scalar) -> Scalar:
        assert (self.location == other.location)
        return Scalar(self.data.where(condition.data, other.data), self.location)

    def swap_location(self, direction: Direction) -> None:
        self.location.swap(direction)

    def left(self, direction: Direction) -> Scalar:
        if direction.name == 'X':
            return Scalar(self.data[:-1, :], self.location)
        else:
            return Scalar(self.data[:, :-1], self.location)

    def right(self, direction: Direction) -> Scalar:
        if direction.name == 'X':
            return Scalar(self.data[1:, :], self.location)
        else:
            return Scalar(self.data[:, 1:], self.location)

    def interior(self, mesh: Mesh) -> Scalar:
        return Scalar(
            self.data[tuple(mesh.interior[self.location[direction]] for direction in Direction)],
            self.location
        )

    def boundary(self, direction: Direction, side: Side, mesh: Mesh) -> Scalar:
        return Scalar(
            self.data[tuple(
                mesh.boundary[self.location[d]][side] if d is direction else slice(None)
                for d in Direction
            )],
            self.location
        )


def scalar_zeros(location: Location, mesh: Mesh) -> Scalar:
    size: list[int] = []
    for direction in Direction:
        if location[direction] is AxisLocation.CENTER:
            size.append(mesh.N + 2*mesh.NGhost)
        else:
            size.append(mesh.N + 1)

    return Scalar(torch.zeros(size), location)


class Vector:
    x: Scalar
    y: Scalar

    def __init__(self, x: Scalar, y: Scalar) -> None:
        self.x = x
        self.y = y

    def add_(self, other: Vector) -> Vector:
        self.x.add_(other.x)
        self.y.add_(other.y)
        return self

    def mul_(self, other: int | float) -> Vector:
        self.x.mul_(other)
        self.y.mul_(other)
        return self

    def copy_(self, other: Vector) -> Vector:
        assert (self.x.location == other.x.location)
        assert (self.y.location == other.y.location)
        self.x.copy_(other.x)
        self.y.copy_(other.y)
        return self

    def zero_(self) -> Vector:
        self.x.zero_()
        self.y.zero_()
        return self

    def norm(self) -> Scalar:
        return (self.x.pow_(2) + self.y.pow_(2)).sqrt_()


class Matrix:
    x: Vector
    y: Vector

    def __init__(self, x: Vector, y: Vector) -> None:
        self.x = x
        self.y = y

    def add_(self, other: Matrix) -> Matrix:
        self.x.add_(other.x)
        self.y.add_(other.y)
        return self

    def mul_(self, other: int | float) -> Matrix:
        self.x.mul_(other)
        self.y.mul_(other)
        return self

    def copy_(self, other: Matrix) -> Matrix:
        assert (self.x.x.location == other.x.x.location)
        assert (self.x.y.location == other.x.y.location)
        assert (self.y.x.location == other.y.x.location)
        assert (self.y.y.location == other.y.y.location)
        self.x.copy_(other.x)
        self.y.copy_(other.y)
        return self

    def zero_(self) -> Matrix:
        self.x.zero_()
        self.y.zero_()
        return self
