from __future__ import annotations

import enum
import torch

from .mesh import mesh


class Direction(enum.Enum):
    X = 0
    Y = 1


class Location(enum.Enum):
    CENTER = 0
    FACE = 1


class Field:
    data: torch.Tensor
    location: tuple[Location, Location]

    def __init__(self, data: torch.Tensor, location: tuple[Location, Location]) -> None:
        self.data = data
        self.location = location

    def __getitem__(self, slices: tuple[slice, ...]) -> Field:
        return Field(self.data[slices], self.location)

    def __add__(self, other: Field) -> Field:
        assert (self.location == other.location)
        return Field(self.data + other.data, self.location)

    def __sub__(self, other: Field) -> Field:
        assert (self.location == other.location)
        return Field(self.data - other.data, self.location)

    def __mul__(self, other: int | float) -> Field:
        return Field(self.data*other, self.location)

    def __rmul__(self, other: int | float) -> Field:
        return self.__mul__(other)

    def __truediv__(self, other: int | float) -> Field:
        return Field(self.data/other, self.location)

    def swap_location(self, dir: Direction):
        if dir.name == 'X':
            if self.location[dir.value].name == 'CENTER':
                self.location = (Location['FACE'], self.location[1])
            else:
                self.location = (Location['CENTER'], self.location[1])
        else:
            if self.location[dir.value].name == 'CENTER':
                self.location = (self.location[0], Location['FACE'])
            else:
                self.location = (self.location[0], Location['CENTER'])


def zeros(location: tuple[Location, Location]) -> Field:
    size: list[int] = []
    for i in range(2):
        if location[i].name == 'CENTER':
            size.append(mesh.N + 2*mesh.NGhost)
        else:
            size.append(mesh.N + 1)

    return Field(torch.zeros(size), location)
