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
