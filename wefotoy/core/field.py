from __future__ import annotations

import torch

from .defs import Direction, Location


class Field:
    data: torch.Tensor
    location: tuple[Location, Location]

    def __init__(self, data: torch.Tensor, location: tuple[Location, Location]) -> None:
        self.data = data
        self.location = location


class Scalar(Field):
    def __init__(self, data: torch.Tensor, location: tuple[Location, Location]) -> None:
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

    def max(self) -> float:
        return self.data.max().item()

    def where(self, condition: Scalar, other: Scalar) -> Scalar:
        assert (self.location == other.location)
        return Scalar(self.data.where(condition.data, other.data), self.location)

    def swap_location(self, direction: Direction) -> None:
        if direction.name == 'X':
            if self.location[direction.value].name == 'CENTER':
                self.location = (Location['FACE'], self.location[1])
            else:
                self.location = (Location['CENTER'], self.location[1])
        else:
            if self.location[direction.value].name == 'CENTER':
                self.location = (self.location[0], Location['FACE'])
            else:
                self.location = (self.location[0], Location['CENTER'])

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
