from __future__ import annotations

import enum


class Direction(enum.Enum):
    X = 0
    Y = 1


class Location:
    _locations: dict[Direction, AxisLocation]

    def __init__(self, x: AxisLocation, y: AxisLocation) -> None:
        self._locations = {
            Direction.X: x,
            Direction.Y: y
        }

    def __getitem__(self, direction: Direction) -> AxisLocation:
        return self._locations[direction]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Location):
            return NotImplemented
        return all(
            self._locations[direction] is other[direction]
            for direction in Direction
        )

    def copy(self) -> Location:
        return Location(self._locations[Direction.X], self._locations[Direction.Y])

    def swap(self, direction: Direction) -> None:
        self._locations[direction] = self._locations[direction].other()


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
    _regions: dict[Direction, AxisRegion]

    def __init__(self, x: AxisRegion, y: AxisRegion) -> None:
        self._regions = {
            Direction.X: x,
            Direction.Y: y
        }

    def __getitem__(self, direction: Direction) -> AxisRegion:
        return self._regions[direction]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Region):
            return NotImplemented
        return all(
            self._regions[direction] is other[direction]
            for direction in Direction
        )

    def copy(self) -> Region:
        return Region(self._regions[Direction.X], self._regions[Direction.Y])

    def to(self, direction: Direction, region: AxisRegion) -> Region:
        self._regions[direction] = region
        return self


class AxisRegion(enum.Enum):
    FULL = 0
    INTERIOR = 1
    BOUNDARY = 2
    ADJACENT = 3
