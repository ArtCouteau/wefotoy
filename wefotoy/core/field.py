from __future__ import annotations

import torch

from .defs import Direction, AxisLocation, Location, AxisRegion, Region, Side
from .mesh import Mesh


class Field:
    data: torch.Tensor
    location: Location
    region: Region

    def __init__(self, data: torch.Tensor, location: Location, region: Region) -> None:
        self.data = data
        self.location = location
        self.region = region


class Scalar(Field):
    def __init__(self, data: torch.Tensor, location: Location, region: Region) -> None:
        super().__init__(data, location, region)

    def __getitem__(self, slices: tuple[slice, ...]) -> Scalar:
        return Scalar(self.data[slices], self.location.copy(), self.region.copy())

    def __add__(self, other: Scalar) -> Scalar:
        assert (self.location == other.location)
        assert (self.region == other.region)
        return Scalar(self.data + other.data, self.location.copy(), self.region.copy())

    def __sub__(self, other: Scalar) -> Scalar:
        assert (self.location == other.location)
        assert (self.region == other.region)
        return Scalar(self.data - other.data, self.location.copy(), self.region.copy())

    def __neg__(self) -> Scalar:
        # Here unsure if data.copy()
        return Scalar(-self.data, self.location.copy(), self.region.copy())

    def __mul__(self, other: int | float | Scalar) -> Scalar:
        if isinstance(other, (int, float)):
            return Scalar(self.data*other, self.location.copy(), self.region.copy())
        else:
            assert (self.location == other.location)
            assert (self.region == other.region)
            return Scalar(self.data*other.data, self.location.copy(), self.region.copy())

    def __rmul__(self, other: int | float | Scalar) -> Scalar:
        return self.__mul__(other)

    def __truediv__(self, other: int | float | Scalar) -> Scalar:
        if isinstance(other, (int, float)):
            return Scalar(self.data/other, self.location.copy(), self.region.copy())
        else:
            assert (self.location == other.location)
            assert (self.region == other.region)
            return Scalar(self.data/other.data, self.location.copy(), self.region.copy())

    def __rtruediv__(self, other: int | float | Scalar) -> Scalar:
        return self.__truediv__(other)

    def __gt__(self, other: int | float | Scalar) -> Scalar:
        if isinstance(other, (int, float)):
            return Scalar(self.data > other, self.location.copy(), self.region.copy())
        else:
            assert (self.location == other.location)
            assert (self.region == other.region)
            return Scalar(self.data > other.data, self.location.copy(), self.region.copy())

    def __lt__(self, other: int | float | Scalar) -> Scalar:
        if isinstance(other, (int, float)):
            return Scalar(self.data < other, self.location.copy(), self.region.copy())
        else:
            assert (self.location == other.location)
            assert (self.region == other.region)
            return Scalar(self.data < other.data, self.location.copy(), self.region.copy())

    def __ge__(self, other: int | float | Scalar) -> Scalar:
        if isinstance(other, (int, float)):
            return Scalar(self.data >= other, self.location.copy(), self.region.copy())
        else:
            assert (self.location == other.location)
            assert (self.region == other.region)
            return Scalar(self.data >= other.data, self.location.copy(), self.region.copy())

    def __le__(self, other: int | float | Scalar) -> Scalar:
        if isinstance(other, (int, float)):
            return Scalar(self.data <= other, self.location.copy(), self.region.copy())
        else:
            assert (self.location == other.location)
            assert (self.region == other.region)
            return Scalar(self.data <= other.data, self.location.copy(), self.region.copy())

    def add_(self, other: int | float | Scalar) -> Scalar:
        if isinstance(other, (int, float)):
            self.data.add_(other)
        else:
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
        return Scalar(self.data.minimum(other.data), self.location.copy(), self.region.copy())

    def max(self) -> float:
        return self.data.max().item()

    def maximum(self, other: Scalar) -> Scalar:
        assert (self.location == other.location)
        return Scalar(self.data.maximum(other.data), self.location.copy(), self.region.copy())

    def where(self, condition: Scalar, other: Scalar) -> Scalar:
        assert (self.location == other.location)
        return Scalar(self.data.where(condition.data, other.data), self.location.copy(), self.region.copy())

    def shift_location_and_region(self, direction: Direction) -> None:
        self.location.swap(direction)
        if self.location[direction] is AxisLocation.CENTER:
            self.region.to(direction, AxisRegion.INTERIOR)
        else:
            self.region.to(direction, AxisRegion.FULL)

    def left(self, direction: Direction) -> Scalar:
        if self.region[direction] is not AxisRegion.FULL:
            raise ValueError(
                f'Cannot take left region along {direction.name}'
                f'(expected FULL, current region: {self.region[direction].name})'
            )
        return Scalar(
            self.data[tuple(
                slice(None, -1) if d is direction else slice(None)
                for d in Direction
            )],
            self.location,
            self.region.copy().to(direction, AxisRegion.SHIFTED)
        )

    def right(self, direction: Direction) -> Scalar:
        if self.region[direction] is not AxisRegion.FULL:
            raise ValueError(
                f'Cannot take left region along {direction.name}'
                f'(expected FULL, current region: {self.region[direction].name})'
            )
        return Scalar(
            self.data[tuple(
                slice(1, None) if d is direction else slice(None)
                for d in Direction
            )],
            self.location,
            self.region.copy().to(direction, AxisRegion.SHIFTED)
        )

    def _interior_slice(self, direction: Direction, mesh: Mesh) -> slice:
        if self.region[direction] is AxisRegion.FULL:
            return mesh.interior[self.location[direction]]
        elif self.region[direction] is AxisRegion.INTERIOR:
            return slice(None)
        else:
            raise ValueError(
                f'Cannot take interior region along {direction.name}'
                f'(expected FULL or INTERIOR, current region: {self.region[direction].name})'
            )

    def interior(self, mesh: Mesh) -> Scalar:
        return Scalar(
            self.data[tuple(
                self._interior_slice(direction, mesh)
                for direction in Direction
            )],
            self.location,
            Region(AxisRegion.INTERIOR, AxisRegion.INTERIOR)
        )

    def boundary(self, direction: Direction, side: Side, mesh: Mesh) -> Scalar:
        if self.region[direction] is not AxisRegion.FULL:
            raise ValueError(
                f'Cannot take boundary region along {direction.name}'
                f'(expected FULL, current region: {self.region[direction].name})'
            )
        return Scalar(
            self.data[tuple(
                mesh.boundary[self.location[d]][side] if d is direction else slice(None)
                for d in Direction
            )],
            self.location,
            self.region.copy().to(direction, AxisRegion.BOUNDARY)
        )

    def adjacent(self, direction: Direction, side: Side, mesh: Mesh) -> Scalar:
        if self.region[direction] is not AxisRegion.FULL:
            raise ValueError(
                f'Cannot take adjacent region along {direction.name}'
                f'(expected FULL, current region: {self.region[direction].name})'
            )
        return Scalar(
            self.data[tuple(
                mesh.adjacent[side] if d is direction else slice(None)
                for d in Direction
            )],
            self.location,
            self.region.copy().to(direction, AxisRegion.ADJACENT)
        )


def scalar_zeros(mesh: Mesh, location: Location, region: Region = Region(AxisRegion.FULL, AxisRegion.FULL)) -> Scalar:
    size: list[int] = []
    for direction in Direction:
        if location[direction] is AxisLocation.CENTER:
            _size = mesh.N
            if region[direction] is AxisRegion.FULL:
                _size += 2*mesh.NGhost
            size.append(_size)
        else:
            size.append(mesh.N + 1)

    return Scalar(torch.zeros(size), location, region)


class Vector:
    _scalars: dict[Direction, Scalar]

    def __init__(self, x: Scalar, y: Scalar) -> None:
        self._scalars = {
            Direction.X: x,
            Direction.Y: y
        }

    def __getitem__(self, direction: Direction) -> Scalar:
        return self._scalars[direction]

    @property
    def x(self) -> Scalar:
        return self[Direction.X]

    @property
    def y(self) -> Scalar:
        return self[Direction.Y]

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

    def interior(self, mesh: Mesh) -> Vector:
        return Vector(self.x.interior(mesh), self.y.interior(mesh))


class Matrix:
    _vectors: dict[Direction, Vector]

    def __init__(self, x: Vector, y: Vector) -> None:
        self._vectors = {
            Direction.X: x,
            Direction.Y: y
        }

    def __getitem__(self, direction: Direction) -> Vector:
        return self._vectors[direction]

    @property
    def x(self) -> Vector:
        return self[Direction.X]

    @property
    def y(self) -> Vector:
        return self[Direction.Y]

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
