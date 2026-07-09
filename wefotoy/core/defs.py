from __future__ import annotations

import enum


class Direction(enum.Enum):
    X = 0
    Y = 1


class Location:
    x: AxisLocation
    y: AxisLocation

    def __init__(self, x: AxisLocation, y: AxisLocation) -> None:
        self.x = x
        self.y = y

    def swap(self, direction: Direction) -> None:
        if direction is Direction.X:
            if self.x is AxisLocation.CENTER:
                self.x = AxisLocation.FACE
            else:
                self.x = AxisLocation.CENTER
        else:
            if self.y is AxisLocation.CENTER:
                self.y = AxisLocation.FACE
            else:
                self.y = AxisLocation.CENTER


class AxisLocation(enum.Enum):
    CENTER = 0
    FACE = 1


class Side(enum.Enum):
    LOWER = 0
    UPPER = 1
