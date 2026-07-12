from __future__ import annotations

import enum


class Direction(enum.Enum):
    X = 0
    Y = 1


class Location:
    _location: dict[Direction, AxisLocation]

    def __init__(self, x: AxisLocation, y: AxisLocation) -> None:
        self._location = {
            Direction.X: x,
            Direction.Y: y
        }

    def __getitem__(self, direction: Direction) -> AxisLocation:
        return self._location[direction]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Location):
            return NotImplemented
        return all(
            self._location[direction] is other[direction]
            for direction in Direction
        )

    def copy(self) -> Location:
        return Location(self._location[Direction.X], self._location[Direction.Y])

    def swap(self, direction: Direction) -> None:
        self._location[direction] = self._location[direction].other()


class AxisLocation(enum.Enum):
    CENTER = 0
    FACE = 1

    def other(self) -> AxisLocation:
        if self is AxisLocation.CENTER:
            return AxisLocation.FACE
        else:
            return AxisLocation.CENTER


class Side(enum.Enum):
    LOWER = 0
    UPPER = 1

    def opposite(self) -> Side:
        if self is Side.LOWER:
            return Side.UPPER
        else:
            return Side.LOWER


class Region:
    _region: dict[Direction, AxisRegion]

    def __init__(self, x: AxisRegion, y: AxisRegion) -> None:
        self._region = {
            Direction.X: x,
            Direction.Y: y
        }

    def __getitem__(self, direction: Direction) -> AxisRegion:
        return self._region[direction]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Region):
            return NotImplemented
        return all(
            self._region[direction] is other[direction]
            for direction in Direction
        )

    def copy(self) -> Region:
        return Region(self._region[Direction.X], self._region[Direction.Y])

    def to(self, direction: Direction, region: AxisRegion) -> Region:
        self._region[direction] = region
        return self


class AxisRegion(enum.Enum):
    FULL = 0
    INTERIOR = 1
    BOUNDARY = 2
    ADJACENT = 3
    SHIFTED = 4
