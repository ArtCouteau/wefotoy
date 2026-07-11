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
        if self._location[direction] is AxisLocation.CENTER:
            self._location[direction] = AxisLocation.FACE
        else:
            self._location[direction] = AxisLocation.CENTER


class AxisLocation(enum.Enum):
    CENTER = 0
    FACE = 1


class Side(enum.Enum):
    LOWER = 0
    UPPER = 1
